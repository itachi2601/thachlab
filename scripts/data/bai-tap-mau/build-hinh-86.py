"""Bài tập mẫu bài 86 "Bài 8. Thấu kính" (KHTN 9) — 5 dạng, chuẩn "một dạng — một hình" (cong_cu họ thau_kinh, de:true).
Quy ước dấu (đúng lý thuyết bài 86): d > 0 (vật thật); f > 0 hội tụ, f < 0 phân kì; d' > 0 ảnh thật, d' < 0 ảnh ảo (cùng phía vật);
1/f = 1/d + 1/d'; k = h'/h = |d'|/d. Hình: cm, y lên, thấu kính tại x = 0, vật ở x = −d.
Mọi đáp số tính lại bằng Fraction trong kiem_so(); mọi lựa chọn sai được assert cho kết quả khác đáp án đúng.
Chạy: python3 scripts/data/bai-tap-mau/build-hinh-86.py   (idempotent, ghi 86.json; không ghi DB). Dạng: 86.dang.md"""
import json, os, sys
from fractions import Fraction as Fr
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "../../../.claude/skills/soan-bai-tap-mau/scripts"))
from dung import sol, tbl, buoc, M, P, A

T86 = "Đặc điểm thấu kính hội tụ, phân kì và tiêu cự"
T87 = "Dựng ảnh của vật qua thấu kính"
T88 = "Công thức thấu kính và số phóng đại"


def anh(f, d):
    """d' theo 1/f = 1/d + 1/d' (Fraction); None nếu ảnh ở vô cực."""
    f, d = Fr(f), Fr(d)
    inv = 1 / f - 1 / d
    return None if inv == 0 else 1 / inv


# ═══════════════ SỐ LIỆU + KIỂM ═══════════════
# D1: kính phân kì, S = F′ cách kính 12 cm cùng phía tia tới, tia trên cùng cách trục 3 cm, hỏi ở 8 cm sau kính
D1_F, D1_H, D1_X = -12, 3, 8
D1_Y = D1_H * Fr(abs(D1_F) + D1_X, abs(D1_F))                   # 5
# D2: hội tụ f = 6, h = 2: a) d = 15; b) d = 4; c) phân kì |f| = 6, d = 15
D2_F, D2_H = 6, 2
D2A_D, D2B_D, D2C_D = 15, 4, 15
D2A_DP = anh(D2_F, D2A_D)                                        # 10
D2B_DP = anh(D2_F, D2B_D)                                        # −12
D2C_DP = anh(-D2_F, D2C_D)                                       # −30/7
D2A_HP = D2_H * abs(D2A_DP) / D2A_D                              # 4/3
D2B_HP = D2_H * abs(D2B_DP) / D2B_D                              # 6
D2C_HP = D2_H * abs(D2C_DP) / D2C_D                              # 4/7
# D3: hội tụ f = 16, h = 3: a) d = 24; b) d = 10
D3_F, D3_H, D3A_D, D3B_D = 16, 3, 24, 10
D3A_DP, D3B_DP = anh(D3_F, D3A_D), anh(D3_F, D3B_D)              # 48 ; −80/3
D3A_HP = D3_H * abs(D3A_DP) / D3A_D                              # 6
D3B_HP = D3_H * abs(D3B_DP) / D3B_D                              # 8
# D4: ảnh ảo cao 2 cm của vật cao 6 cm cách kính 36 cm
D4_H, D4_HP, D4_D = 6, 2, 36
D4_DP = -(Fr(D4_HP, D4_H) * D4_D)                                # −12
D4_F = 1 / (Fr(1, D4_D) + 1 / D4_DP)                             # −18
# D5: hội tụ f = 18, h = 1,5; ảnh thật k = 3; rồi dịch vật ra xa 6 cm
D5_F, D5_H, D5_K, D5_DICH = 18, Fr(3, 2), 3, 6
D5_D = D5_F * (1 + Fr(1, D5_K))                                  # 24
D5_DP = D5_K * D5_D                                              # 72
D5_HP = D5_H * D5_K                                              # 9/2
D5_D2 = D5_D + D5_DICH                                           # 30
D5_D2P = anh(D5_F, D5_D2)                                        # 45
D5_H2P = D5_H * D5_D2P / D5_D2                                   # 9/4
D5_LECH = D5_DP - D5_D2P                                         # 27


def kiem_so():
    assert (D1_Y, ) == (5, )
    assert (D2A_DP, D2B_DP, D2A_D > 2 * D2_F, D2B_D < D2_F) == (10, -12, True, True)
    assert D2C_DP < 0 and abs(D2C_DP) < D2_F and D2C_HP < D2_H                  # phân kì: ảo, nhỏ, nằm giữa O và F′
    assert D2A_HP == Fr(4, 3) and D2B_HP == 6
    assert (D3A_DP, D3A_HP, D3B_DP, D3B_HP) == (48, 6, Fr(-80, 3), 8)
    assert D3A_D > D3_F > D3B_D
    # lựa chọn sai D3
    assert 1 / (Fr(1, D3_F) + Fr(1, D3A_D)) != D3A_DP                           # cộng thay vì trừ → 9,6
    assert D3_F - D3A_D != D3A_DP and abs(D3A_DP) != D3_H * D3A_D / abs(D3A_DP)
    assert D3_H * Fr(D3A_D) / abs(D3A_DP) != D3A_HP                              # tỉ số ngược → 1,5
    assert D3_H * abs(D3A_DP) / D3_F != D3A_HP
    assert D3_H * Fr(D3B_D, 1) / abs(D3B_DP) != D3B_HP
    # D4
    assert (D4_DP, D4_F) == (-12, -18) and D4_F < 0 and abs(D4_DP) < abs(D4_F)
    assert 1 / (Fr(1, D4_D) + Fr(1, 12)) != D4_F                                 # thế d′ dương → f = 9
    assert Fr(D4_D * D4_DP, D4_D - D4_DP) != D4_F                                # f = dd′/(d − d′) → −9
    # D5
    assert (D5_D, D5_DP, D5_HP, D5_D2, D5_D2P, D5_H2P, D5_LECH) == (24, 72, Fr(9, 2), 30, 45, Fr(9, 4), 27)
    assert Fr(1, D5_F) == Fr(1, D5_D) + Fr(1, D5_DP) and Fr(1, D5_F) == Fr(1, D5_D2) + Fr(1, D5_D2P)
    assert D5_F * (1 + D5_K) != D5_D and Fr(D5_F, D5_K) != D5_D and D5_D + D5_F != D5_DP
    assert D5_DP != D5_D2P and D5_D2P < D5_DP                                    # vật ra xa → ảnh thật lại gần kính
    assert D5_D - D5_DICH != D5_D2 and D5_DP + D5_DICH != D5_D2P


# ═══════════════ HÌNH (cong_cu, de:true) ═══════════════
def tk(kieu, f=None, **kw):
    d = {"loai": "tk", "x": 0, "kieu": kieu}
    if f is not None:
        d["f"] = f
        d["vi_tieu"] = ["b", "b"]
    d.update(kw)
    return d


def vat(x, h, **kw):
    return dict({"loai": "vat", "x": x, "h": h}, **kw)


def tia(qua, mau=None, keo=None, **kw):
    d = {"loai": "tia", "qua": qua}
    if mau:
        d["mau"] = mau
    if keo:
        d["keo"] = keo
    d.update(kw)
    return d


def ghi(t):
    return {"loai": "ghi", "text": t}


def thuoc(tu, den, o, nhan, doc=False, ben=None, **kw):
    d = {"loai": "thuoc", "tu": tu, "den": den, "o": o, "nhan": nhan}
    if doc:
        d["doc"] = True
    if ben:
        d["ben"] = ben
    d.update(kw)
    return d


def diem(x, ten, y=0, vi_="b", **kw):
    return dict({"loai": "diem", "x": x, "y": y, "ten": ten, "vi": vi_}, **kw)


def chu(x, y, text, a="start", **kw):
    return dict({"loai": "chu", "x": x, "y": y, "text": text, "a": a}, **kw)


def pho(phan, lop):
    return {"loai": "thau_kinh", "de": True, "phan": phan, "lop": lop}


def cong_cu_1():
    # lớp 0: kính CHƯA rõ loại (thước dọc "L"), ba tia song song tới; S và độ cao đề cho
    hinh = [thuoc(-7.2, 7.2, 0, "L", doc=True, ben="phai", het=1)]
    hinh += [tia([[-26, y], [0, y]]) for y in (3, 0, -3)]
    hinh += [diem(-12, "S"), thuoc(-12, 0, -4.5, "12 cm", ben="duoi"), chu(-27, 4.4, "cách trục 3 cm")]
    ph = [{"tu_buoc": 0, "x_min": -28, "x_max": 22, "y_tren": 7.5, "y_duoi": -7.5, "hinh": hinh}]
    lop = [
        [tk("phan_ki", ten="L", ten_ben="phai"), diem(0, "O", vi_="t"), ghi("Chùm loe ra sau kính: thấu kính phân kì")],
        [ghi("S là tiêu điểm F′ (cùng phía chùm tới): f = −12 cm")],
        [tia([[0, 3], [14, 6.5]], "max", keo=[[-12, 0], [0, 3]]), tia([[0, -3], [14, -6.5]], "max", keo=[[-12, 0], [0, -3]]),
         tia([[0, 0], [14, 0]], "max"), thuoc(0, 5, 8, "5 cm", doc=True, ben="phai"),
         ghi("Tia ló loe ra: cách trục 5 cm tại 8 cm sau kính")],
    ]
    return pho(ph, lop)


def cong_cu_2():
    # a) f = 6, d = 15 (hội tụ); b) d = 4; c) phân kì |f| = 6, d = 15. Hình đề không vẽ sẵn ảnh.
    A = {"tu_buoc": 0, "x_min": -20, "x_max": 20, "y_tren": 3, "y_duoi": -4, "phong_doc": 2,
         "hinh": [tk("hoi_tu", 6), vat(-15, 2), thuoc(-15, 0, -2.2, "d = 15 cm", ben="duoi"), chu(-13.6, 1.0, "AB = 2 cm")]}
    B = {"tu_buoc": 1, "x_min": -18, "x_max": 14, "y_tren": 7.5, "y_duoi": -3.2, "phong_doc": 1,
         "hinh": [tk("hoi_tu", 6), vat(-4, 2), thuoc(-4, 0, -2.0, "d = 4 cm", ben="duoi")]}
    C = {"tu_buoc": 3, "x_min": -20, "x_max": 12, "y_tren": 3, "y_duoi": -2.4, "phong_doc": 1.6,
         "hinh": [tk("phan_ki", 6), vat(-15, 2), thuoc(-15, 0, -1.6, "d = 15 cm", ben="duoi")]}
    xa = float(D2A_DP)
    lop = [
        [tia([[-15, 2], [0, 0], [14, -14 * 2 / 15]], "max"),
         tia([[-15, 2], [0, 2], [xa, float(-D2A_HP)]], "max"),
         vat(xa, -float(D2A_HP), mau="max", ten=["A′", "B′"]), ghi("Ảnh thật, ngược chiều, nhỏ hơn vật")],
        [tia([[-4, 2], [0, 0], [14, -7]], "max", keo=[[0, 0], [-12, 6]]),
         tia([[-4, 2], [0, 2], [10, 2 - 10 / 3]], "max", keo=[[0, 2], [-12, 6]]),
         ghi("Hai tia ló loe ra, không cắt nhau sau kính")],
        [vat(-12, 6, ao=True, mau="max", ten=["A′", "B′"]), ghi("Ảnh ảo, cùng chiều, lớn hơn vật (B′ ở nét đứt)")],
        [tia([[-15, 2], [0, 2], [10, 2 + 10 / 3]], "max", keo=[[-6, 0], [0, 2]]),
         ghi("Tia ló có đường kéo dài đi qua F′ (cùng phía với vật)")],
        [tia([[-15, 2], [0, 0], [10, -2 * 10 / 15]], "max"),
         vat(float(D2C_DP), float(D2C_HP), ao=True, mau="max", ten=["A′", "B′"]),
         ghi("Ảnh ảo, cùng chiều, nhỏ hơn vật, nằm giữa O và F′")],
    ]
    return pho([A, B, C], lop)


def cong_cu_3():
    A = {"tu_buoc": 0, "x_min": -32, "x_max": 78, "y_tren": 4.2, "y_duoi": -7.5, "phong_doc": 3.5,
         "hinh": [tk("hoi_tu", 16), vat(-24, 3), thuoc(-24, 0, -3.4, "d = 24 cm", ben="duoi"), chu(-22.5, 2.2, "h = 3 cm")]}
    B = {"tu_buoc": 3, "x_min": -48, "x_max": 26, "y_tren": 9.8, "y_duoi": -6.5, "phong_doc": 1.8,
         "hinh": [tk("hoi_tu", 16), vat(-10, 3), thuoc(-10, 0, -4, "d = 10 cm", ben="duoi"), chu(-8.6, 2.0, "h = 3 cm")]}
    bx = float(D3B_DP)
    lop = [
        [ghi("d lớn hơn f: vật ngoài tiêu điểm → ảnh thật, d′ dương")],
        [tia([[-24, 3], [0, 0], [48, -6]], "max"), tia([[-24, 3], [0, 3], [48, -6]], "max"),
         vat(48, -6, mau="max", ten=["A′", "B′"]), ghi("d′ = 48 cm · ảnh thật, ngược chiều")],
        [thuoc(0, -6, 52, "h′ = 6 cm", doc=True, ben="phai"), ghi("k = 2 → h′ = 6 cm")],
        [ghi("d nhỏ hơn f: ảnh ảo, cùng chiều, lớn hơn vật")],
        [tia([[-10, 3], [0, 0], [14, -4.2]], "max", keo=[[0, 0], [bx, 8]]),
         tia([[-10, 3], [0, 3], [16, 0], [22, -1.125]], "max", keo=[[0, 3], [bx, 8]]),
         vat(bx, 8, ao=True, mau="max", ten=["A′", "B′"]), ghi("d′ ≈ −26,7 cm: ảnh ảo, cách kính 26,7 cm")],
        [thuoc(0, 8, bx - 3, "h′ = 8 cm", doc=True, ben="trai"), ghi("k = 8/3 → h′ = 8 cm")],
    ]
    return pho([A, B], lop)


def cong_cu_4():
    hinh = [thuoc(-3.8, 9.6, 0, "L", doc=True, ben="phai", het=1), vat(-36, 6), thuoc(-36, 0, -4, "d = 36 cm", ben="duoi"),
            chu(-34.5, 3.0, "AB = 6 cm")]
    ph = [{"tu_buoc": 0, "x_min": -44, "x_max": 24, "y_tren": 9.8, "y_duoi": -6.5, "phong_doc": 1.8, "hinh": hinh}]
    lop = [
        [tk("phan_ki", ten="L", ten_ben="phai"), diem(0, "O", vi_="t"), ghi("Ảnh ảo nhỏ hơn vật: thấu kính phân kì")],
        [tia([[-36, 6], [0, 0], [14, -14 / 6]], "max"), vat(-12, 2, ao=True, mau="max", ten=["A′", "B′"]),
         ghi("d′ = −12 cm: ảnh ảo, cùng phía vật")],
        [diem(-18, "F′"), tia([[-36, 6], [0, 6], [6, 8]], "max", keo=[[-18, 0], [0, 6]]),
         ghi("f = −18 cm: F′ cùng phía vật")],
        [ghi("|d′| = 12 cm nhỏ hơn |f| = 18 cm: ảnh nằm giữa O và F′")],
    ]
    return pho(ph, lop)


def cong_cu_5():
    hinh = [tk("hoi_tu", 18), vat(-44, 1.5, het=2), chu(-49, -3.2, "AB = 1,5 cm", het=2)]
    ph = [{"tu_buoc": 0, "x_min": -50, "x_max": 82, "y_tren": 3.4, "y_duoi": -7, "phong_doc": 5, "hinh": hinh}]
    lop = [
        [ghi("Ảnh rõ trên màn là ảnh thật: d′ dương, d′ = 3d")],
        [vat(-24, 1.5, ten=["A", "B"], het=4), thuoc(-24, 0, -3.4, "d = 24 cm", ben="duoi", het=4), ghi("Vật ở P cách kính 24 cm")],
        [tia([[-24, 1.5], [0, 0], [78, -4.875]], "max", het=4), tia([[-24, 1.5], [0, 1.5], [72, -4.5]], "max", het=4),
         vat(72, -4.5, mau="max", ten=["A′", "B′"], het=4), ghi("Màn cách kính 72 cm · ảnh cao 4,5 cm")],
        [vat(-30, 1.5, ten=["A_2", "B_2"]), thuoc(-30, 0, -3.4, "d_2 = 30 cm", ben="duoi"), ghi("Vật dịch ra xa 6 cm: d_2 = 30 cm")],
        [tia([[-30, 1.5], [0, 0], [78, -3.9]], "max"), tia([[-30, 1.5], [0, 1.5], [45, -2.25]], "max"),
         vat(45, -2.25, mau="max", ten=["A_2′", "B_2′"]), ghi("Ảnh mới ở 45 cm sau kính")],
        [vat(72, -4.5, ao=True, mau="min", ten=["", ""]), ghi("Vật ra xa → ảnh thật lại gần kính (màn dịch lại gần)")],
        [thuoc(45, 72, 2.4, "27 cm", ben="tren"), ghi("Màn dịch lại gần kính 27 cm")],
        [thuoc(0, -2.25, 49, "2,25 cm", doc=True, ben="phai"), ghi("h_2′ = 2,25 cm")],
    ]
    return pho(ph, lop)


# ═══════════════ NỘI DUNG CÁC DẠNG ═══════════════
QUY_UOC = r"Quy ước dấu: $d\gt0$; $f\gt0$ kính hội tụ, $f\lt0$ kính phân kì; $d'\gt0$ ảnh thật, $d'\lt0$ ảnh ảo; $k=\dfrac{h'}{h}=\dfrac{|d'|}{d}$"
CT = r"$\dfrac1f=\dfrac1d+\dfrac1{d'}$"


def dang(label, topic, form, cap, fading, nhan_dang, tom_de, problem, analysis, hinh, steps, recall, finals, note, go_roi):
    """steps: list dict(tieu_de, buoc=<kwargs của dung.buoc>, sol=[(kind, text)…])."""
    b = [buoc(s["tieu_de"], **s["buoc"]) for s in steps]
    sol_html = sol(recall, [(s["tieu_de"], s["sol"]) for s in steps], finals, note)
    assert len(hinh["lop"]) == len(b), (label, len(hinh["lop"]), len(b))
    return {"form": form, "label": label, "topic": topic, "problem_html": problem, "analysis_html": tbl(analysis),
            "solution_html": sol_html, "nhan_dang": nhan_dang, "cap_do": cap, "fading": fading, "go_roi": {"buoc_hay_sai": go_roi},
            "buoc": b, "tom_de": tom_de, "cong_cu": hinh}


# ───────── Dạng 1 ─────────
D1 = dang(
    "Dạng 1 · Dễ · Nhận biết loại thấu kính và tiêu cự từ chùm tia song song", T86, "ly_thuyet", 1, "mo_het",
    r"Thấy <b>chùm song song loe ra sau kính</b> → nghĩ tới <b>thấu kính phân kì, $f\lt0$</b>",
    {"cho": [r"3 tia song song trục chính; tia trên cùng cách trục $3$ cm", r"đường kéo dài tia ló cắt trục tại $S$, $OS=12$ cm, cùng phía chùm tới"],
     "tim": [r"a) loại kính, $f$ (có dấu)", r"b) tia ló trên cùng cách trục bao nhiêu cm tại điểm cách kính $8$ cm phía sau"]},
    r'<p>Một hộp đèn phát ba tia sáng song song với trục chính tới thấu kính $L$ (chưa biết loại); tia trên cùng cách trục chính $3\ \text{cm}$. '
    r'Sau $L$, ba tia loe ra; đường kéo dài của các tia ló gặp nhau tại điểm $S$ trên trục chính, cách $L$ một đoạn $12\ \text{cm}$ và nằm cùng phía với chùm tia tới.</p>'
    r'<ol type="a"><li>$L$ là thấu kính loại nào? Tiêu cự $f$ của $L$ bằng bao nhiêu (theo quy ước dấu)?</li>'
    r'<li>Tại điểm cách $L$ $8\ \text{cm}$ về phía sau kính, tia ló trên cùng cách trục chính bao nhiêu cm?</li></ol>',
    [(r'"ba tia sáng song song với trục chính tới thấu kính $L$"', r"Chùm tới song song trục", r"Tia song song trục qua thấu kính thì tia ló đi thế nào, tuỳ loại kính?"),
     (r'"Sau $L$, ba tia loe ra"', r"Chùm ló phân kì", r"Chùm song song gom lại hay toả ra thì là loại kính nào?"),
     (r'"đường kéo dài ... gặp nhau tại $S$ ... cùng phía với chùm tia tới"', r"$OS=12$ cm", r"⚠ $S$ nằm trước hay sau kính? Điểm đó có tên gì, và dấu của $f$ theo quy ước là gì?"),
     (r'"tia trên cùng cách trục chính $3\ \text{cm}$"', r"Độ cao tia tới $=3$ cm", r"Tia ló trên cùng nằm trên đường thẳng nối hai điểm nào?"),
     (r'"cách $L$ $8\ \text{cm}$ về phía sau ... cách trục chính bao nhiêu cm"', r"Cần độ cao $y$ tại $8$ cm sau kính", r"Hai tam giác nào có chung đỉnh $S$ để so sánh độ cao?")],
    cong_cu_1(),
    [
        dict(tieu_de="Nhận biết loại thấu kính",
             buoc=dict(hoi="Thấu kính L thuộc loại nào?",
                       lua_chon=[("Thấu kính phân kì: chùm song song loe ra sau kính", True),
                                 ("Thấu kính hội tụ", "Thấu kính hội tụ làm chùm song song gom lại, các tia ló gặp nhau thật phía sau kính; ở đây chỉ đường kéo dài mới gặp nhau."),
                                 ("Chưa kết luận được vì chưa biết rìa kính dày hay mỏng", "Nhận biết bằng chùm song song cũng đủ: loe ra là phân kì, gom lại là hội tụ.")],
                       loi="Thấy có một điểm gặp nhau ($S$) nên cho là hội tụ, quên rằng ở đây chỉ đường kéo dài của tia ló gặp nhau."),
             sol=[("p", "Chùm tới song song trục, chùm ló <b>loe ra</b>, nên $L$ là thấu kính phân kì (rìa dày)."),
                  ("a", "T:Thấu kính phân kì.")]),
        dict(tieu_de="Tiêu cự và dấu của f",
             buoc=dict(hoi="Tiêu cự f của L bằng bao nhiêu cm (có dấu)?", dap_so=-12, don_vi="cm", sai_so=0.5,
                       loi="Lấy $f=+12$ cm vì tiêu cự là một độ dài, quên rằng phân kì phải thay $f$ âm vào công thức.",
                       ke=[(r"Đọc $OS$ là độ dài $OF'$, rồi gán dấu theo loại kính", True),
                           (r"Lấy $f$ dương vì tiêu cự là một độ dài", r"Độ dài thì dương, nhưng dấu của $f$ trong công thức mang thông tin loại kính: phân kì thì $f\lt0$."),
                           (r"Lấy $f$ bằng độ cao $3$ cm của tia tới", r"$3$ cm là khoảng cách từ tia tới đến trục, không phải khoảng cách $OS$.")]),
             sol=[("p", r"Tia tới song song trục, tia ló có đường kéo dài qua tiêu điểm $F'$. Vậy $S$ chính là $F'$, nên $OF'=OS=12\ \text{cm}$."),
                  ("p", "Kính phân kì: lấy $f$ âm."),
                  ("a", r"f=-12\ \text{cm}")]),
        dict(tieu_de="Độ cao tia ló tại điểm cách kính 8 cm",
             buoc=dict(hoi="Tại điểm cách L 8 cm phía sau, tia ló trên cùng cách trục bao nhiêu cm?", dap_so=5, don_vi="cm", sai_so=0.2,
                       loi="Coi tia ló vẫn song song trục nên vẫn cách trục $3$ cm, hoặc cộng thẳng $3+8$.",
                       ke=[(r"Hai tam giác chung đỉnh $S$: độ cao tỉ lệ với khoảng cách tới $S$, tức $\dfrac{y}{3}=\dfrac{OS+8}{OS}$", True),
                           (r"Tia ló cũng song song trục nên $y=3$ cm", r"Chỉ tia tới song song trục; tia ló của kính phân kì loe ra, càng xa kính càng cách trục nhiều."),
                           (r"Cộng thẳng $y=3+8$", r"Độ cao tăng tỉ lệ với khoảng cách tới $S$; không cộng được độ cao (cm) với quãng đường đi thêm theo phương khác.")]),
             sol=[("p", r"Tia ló trên cùng nằm trên đường thẳng qua $S$ và điểm tới kính (cách trục $3$ cm). Hai tam giác vuông chung đỉnh $S$ đồng dạng:"),
                  ("m", r"\dfrac{y}{3}=\dfrac{OS+8}{OS}"),
                  ("m", r"y=3\cdot\dfrac{12+8}{12}"),
                  ("a", r"y=5\ \text{cm}"),
                  ("p", "Kiểm tra: tia ló loe ra nên $y\\gt3$ cm. Hợp lí.")]),
    ],
    ["<b>Thấu kính phân kì</b>: chùm song song loe ra; đường kéo dài tia ló qua $F'$ (cùng phía chùm tới), $OF'=OF=|f|$.",
     r"<b>Quy ước dấu</b>: $f\gt0$ kính hội tụ, $f\lt0$ kính phân kì.",
     "<b>Tam giác đồng dạng</b>: độ cao tia ló tỉ lệ với khoảng cách tới $F'$."],
    [r"a) Thấu kính phân kì, $f=-12\ \text{cm}$", r"b) Tia ló trên cùng cách trục $5\ \text{cm}$"],
    r"Dạng này nhận ra khi: chùm song song trục tới một kính chưa biết loại → xem chùm ló gom hay loe, rồi đọc $OF'$ và gán dấu.",
    1)

# ───────── Dạng 2 ─────────
D2 = dang(
    "Dạng 2 · Trung bình · Dựng ảnh bằng hai tia đặc biệt, nêu tính chất ảnh theo vị trí vật", T87, "ly_thuyet", 2, "giau_buoc_cuoi",
    r"Thấy <b>nêu tính chất ảnh theo vị trí vật</b> → so <b>$d$ với $f$ và $2f$</b>, rồi dựng hai tia từ $B$",
    {"cho": [r"hội tụ $f=6$ cm; $AB=2$ cm", r"a) $d=15$ cm · b) $d=4$ cm", r"c) phân kì $|f|=6$ cm, $d=15$ cm"],
     "tim": ["a) tính chất ảnh", "b) tính chất ảnh, cách xác định ảnh", r"c) tính chất ảnh, vị trí so với $O$ và $F'$"]},
    r'<p>Thấu kính hội tụ có tiêu cự $f=6\ \text{cm}$. Vật sáng $AB$ cao $2\ \text{cm}$ đặt vuông góc với trục chính, $A$ nằm trên trục chính.</p>'
    r'<ol type="a"><li>$AB$ cách thấu kính $15\ \text{cm}$. Dựng ảnh $A\'B\'$ bằng hai tia đặc biệt và nêu tính chất ảnh.</li>'
    r'<li>Dịch $AB$ lại gần, cách thấu kính $4\ \text{cm}$. Nêu tính chất ảnh và cách xác định ảnh trên hình vẽ.</li>'
    r'<li>Thay thấu kính hội tụ bằng thấu kính phân kì có $|f|=6\ \text{cm}$, đặt $AB$ cách thấu kính $15\ \text{cm}$. Nêu tính chất ảnh và vị trí của ảnh so với $O$ và $F\'$.</li></ol>',
    [(r'"hội tụ có tiêu cự $f=6\ \text{cm}$"', r"$f=6$ cm; $2f=12$ cm", r"⚠ Điều kiện để dùng bảng tính chất ảnh: cần so $d$ với những giá trị nào của kính?"),
     (r'"$AB$ cách thấu kính $15\ \text{cm}$"', r"$d=15$ cm", r"$d$ nằm ngoài $2f$, giữa $f$ và $2f$, hay trong $f$?"),
     (r'"Dựng ảnh ... bằng hai tia đặc biệt"', r"Hai trong ba tia", r"Chọn hai tia nào dễ vẽ nhất? Hai tia ló cắt nhau ở đâu?"),
     (r'"Dịch $AB$ lại gần, cách thấu kính $4\ \text{cm}$"', r"$d=4$ cm", r"So lại $d$ với $f$: hai tia ló lúc này còn cắt nhau sau kính không?"),
     (r'"Thay bằng thấu kính phân kì ... $|f|=6\ \text{cm}$"', r"phân kì, $d=15$ cm", r"Tia song song trục qua kính phân kì có đường kéo dài đi qua điểm nào?"),
     (r'"vị trí của ảnh so với $O$ và $F\'$"', r"Cần so $|d'|$ với $|f|$", r"Vật thật qua kính phân kì cho ảnh loại nào, lớn hay nhỏ hơn vật?")],
    cong_cu_2(),
    [
        dict(tieu_de="Câu a: tính chất ảnh",
             buoc=dict(hoi="Câu a, ảnh A′B′ có tính chất gì?",
                       lua_chon=[("Ảnh thật, ngược chiều, nhỏ hơn vật", True),
                                 ("Ảnh thật, ngược chiều, lớn hơn vật", r"Ảnh thật lớn hơn vật chỉ khi $f\lt d\lt2f$; ở đây $d$ lớn hơn $2f$."),
                                 ("Ảnh ảo, cùng chiều, lớn hơn vật", r"Ảnh ảo chỉ có khi vật trong khoảng $OF$ ($d\lt f$); ở đây vật ngoài $F$.")],
                       loi=r"Thấy $d\gt f$ rồi kết luận 'lớn hơn' mà chưa so $d$ với $2f$."),
             sol=[("p", r"So sánh: $f=6\ \text{cm}$, $2f=12\ \text{cm}$, $d=15\ \text{cm}$ nên $d\gt2f$."),
                  ("p", "Dựng: tia từ $B$ qua $O$ đi thẳng; tia từ $B$ song song trục ló qua $F'$. Hai tia ló cắt nhau thật sau kính tại $B'$, hạ vuông góc xuống trục được $A'$."),
                  ("a", "T:Ảnh thật, ngược chiều, nhỏ hơn vật.")]),
        dict(tieu_de="Câu b: vật trong tiêu cự",
             buoc=dict(hoi="Câu b, ảnh A′B′ có tính chất gì?",
                       lua_chon=[("Ảnh ảo, cùng chiều, lớn hơn vật", True),
                                 ("Ảnh thật, ngược chiều, lớn hơn vật", "Hai tia ló loe ra, không cắt nhau thật nên không có ảnh thật."),
                                 ("Không có ảnh vì vật quá gần kính", r"Chỉ không có ảnh khi vật đúng tại $F$ ($d=f$); vật trong $OF$ vẫn cho ảnh ảo.")],
                       loi="Vẫn vẽ hai tia ló cắt nhau sau kính như câu a, không so lại $d$ với $f$.",
                       ke=[(r"So $d$ với $f$ trước: $d\lt f$ nên hai tia ló loe ra", True),
                           ("Vẽ hai tia ló cắt nhau sau kính như câu a", "Ở câu a hai tia ló cắt nhau vì $d\\gt f$; câu b tia ló loe ra, không cắt nhau thật."),
                           ("Vẽ thêm tia thứ ba rồi tìm giao điểm ba tia ló", "Dù vẽ thêm tia nào, các tia ló vẫn loe ra; không có giao điểm thật.")]),
             sol=[("p", r"$d=4\ \text{cm}\lt f=6\ \text{cm}$: vật nằm trong khoảng $OF$. Tia từ $B$ qua $O$ đi thẳng; tia song song trục vẫn ló qua $F'$. Hai tia ló <b>loe ra</b>."),
                  ("a", "T:Ảnh ảo, cùng chiều, lớn hơn vật.")]),
        dict(tieu_de="Câu b: xác định ảnh ảo trên hình",
             buoc=dict(hoi="Trên hình, điểm B′ được xác định thế nào?",
                       lua_chon=[("Kéo dài ngược hai tia ló (nét đứt); giao điểm là B′", True),
                                 ("Lấy giao điểm hai tia ló sau kính", "Hai tia ló loe ra, không có giao điểm sau kính."),
                                 ("Lấy điểm đối xứng của B qua O", "Đối xứng chỉ đúng với gương phẳng; với thấu kính vị trí ảnh phụ thuộc $f$ và $d$.")],
                       loi="Vẽ ảnh ảo bằng nét liền hoặc lấy điểm đối xứng của vật qua $O$.",
                       ke=[("Kéo dài ngược các tia ló về phía vật bằng nét đứt", True),
                           ("Vẽ thêm tia ló dài hơn về phía sau kính", "Kéo dài về phía sau kính vẫn không cắt nhau; phải kéo dài ngược về phía vật."),
                           ("Dùng thước đo từ $B$ sang bên kia $O$ cùng khoảng", "Đó là cách vẽ ảnh qua gương phẳng, không áp dụng cho thấu kính.")]),
             sol=[("p", "Các tia ló không gặp nhau; <b>đường kéo dài ngược</b> của chúng (nét đứt) gặp nhau tại $B'$. Hạ vuông góc từ $B'$ xuống trục được $A'$."),
                  ("a", "T:Ảnh ảo vẽ nét đứt, nằm cùng phía với vật.")]),
        dict(tieu_de="Câu c: tia song song trục qua kính phân kì",
             buoc=dict(hoi="Tia tới song song trục qua kính phân kì, đường kéo dài của tia ló đi qua điểm nào?",
                       lua_chon=[("Tiêu điểm F′ nằm cùng phía với vật", True),
                                 ("Tiêu điểm nằm phía sau kính", "Kính phân kì làm tia ló loe ra, nên chỉ đường kéo dài ngược về phía vật mới gặp trục; $F'$ nằm phía có vật."),
                                 ("Quang tâm O", "Tia qua $O$ mới đi thẳng; tia song song trục ló theo hướng đường kéo dài qua $F'$.")],
                       loi="Vẽ tia ló của kính phân kì đi qua tiêu điểm phía sau kính như kính hội tụ.",
                       ke=[("Nhớ lại: kính phân kì làm chùm song song loe ra", True),
                           ("Dùng ngay cách vẽ của kính hội tụ cho tia này", "Kính hội tụ gom tia ló qua tiêu điểm phía sau; kính phân kì làm tia ló loe ra."),
                           ("Coi tia ló song song với trục", "Tia ló song song trục là tia tới đi qua tiêu điểm của kính hội tụ, không phải trường hợp này.")]),
             sol=[("p", r"Kính phân kì: tia tới song song trục có tia ló loe ra, đường kéo dài ngược đi qua $F'$ nằm <b>cùng phía với vật</b>."),
                  ("a", "T:Kéo dài tia ló (nét đứt) qua $F'$.")]),
        dict(tieu_de="Câu c: tính chất ảnh qua kính phân kì",
             buoc=dict(hoi="Câu c, ảnh có tính chất và vị trí thế nào?",
                       lua_chon=[("Ảnh ảo, cùng chiều, nhỏ hơn vật, nằm giữa O và F′", True),
                                 ("Ảnh thật, ngược chiều, nhỏ hơn vật", "Với vật thật, thấu kính phân kì không cho ảnh thật."),
                                 ("Ảnh ảo, cùng chiều, lớn hơn vật", "Ảnh ảo lớn hơn vật là của kính hội tụ khi vật trong $OF$; kính phân kì luôn cho ảnh nhỏ hơn vật.")],
                       loi="Dùng kết luận 'ảnh ảo thì lớn hơn vật' của kính hội tụ cho kính phân kì.",
                       ke=[("Dựng hai tia như trước, nhưng kéo dài ngược tia ló qua $F'$", True),
                           ("So $d$ với $2f$ rồi áp bảng của kính hội tụ", "Bảng theo $d$ và $2f$ chỉ dành cho kính hội tụ; kính phân kì luôn cho một loại ảnh."),
                           ("Chỉ dựa vào việc $d$ lớn để kết luận ảnh thật", "Ảnh thật cần tia ló gặp nhau thật; kính phân kì không làm được điều đó.")]),
             sol=[("p", "Hai tia ló loe ra; đường kéo dài ngược gặp nhau tại $B'$ nằm trong khoảng từ $O$ đến $F'$."),
                  ("a", "T:Ảnh ảo, cùng chiều, nhỏ hơn vật, nằm giữa $O$ và $F'$.")]),
    ],
    [r"<b>Ảnh thật</b>: tia ló gặp nhau; <b>ảnh ảo</b>: đường kéo dài gặp nhau (nét đứt).",
     r"<b>Kính hội tụ</b>: $d\gt2f$ thật, ngược, nhỏ; $f\lt d\lt2f$ thật, ngược, lớn; $d\lt f$ ảo, cùng chiều, lớn.",
     r"<b>Kính phân kì</b>: luôn ảo, cùng chiều, nhỏ hơn vật, giữa $O$ và $F'$.",
     "<b>Hai tia</b>: qua $O$ đi thẳng; song song trục ló qua $F'$ (phân kì: kéo dài qua $F'$)."],
    ["a) Ảnh thật, ngược chiều, nhỏ hơn vật", "b) Ảnh ảo, cùng chiều, lớn hơn vật; B′ là giao của hai đường kéo dài", "c) Ảnh ảo, cùng chiều, nhỏ hơn vật, nằm giữa $O$ và $F'$"],
    r"Dạng này nhận ra khi: đề hỏi 'tính chất ảnh' hoặc 'dựng ảnh' → so $d$ với $f$, $2f$ của kính hội tụ; kính phân kì luôn ảnh ảo nhỏ.",
    1)

# ───────── Dạng 3 ─────────
D3 = dang(
    "Dạng 3 · Trung bình · Cho f và d, tìm vị trí, độ cao và tính chất ảnh (vật ngoài rồi trong tiêu cự)", T88, "bai_tap", 2, "giau_buoc_cuoi",
    r"Thấy <b>cho $f$, $d$, $h$; tìm ảnh</b> → <b>$\dfrac1{d'}=\dfrac1f-\dfrac1d$</b>, rồi $k=\dfrac{|d'|}{d}$ và đọc dấu $d'$",
    {"cho": [r"hội tụ $f=16$ cm; $AB=3$ cm", r"a) $d=24$ cm · b) $d=10$ cm"],
     "tim": [r"a) $d'$, $h'$", r"b) $d'$ (có dấu), $h'$, tính chất ảnh"]},
    r'<p>Thấu kính hội tụ có tiêu cự $16\ \text{cm}$. Vật sáng $AB$ cao $3\ \text{cm}$ đặt vuông góc với trục chính, $A$ nằm trên trục chính. '
    r"Dùng quy ước: $d'\gt0$ ảnh thật, $d'\lt0$ ảnh ảo.</p>"
    r'<ol type="a"><li>$AB$ cách thấu kính $24\ \text{cm}$. Tìm vị trí và chiều cao của ảnh.</li>'
    r'<li>Dịch $AB$ lại cách thấu kính $10\ \text{cm}$. Tìm vị trí (có dấu) và chiều cao của ảnh; ảnh có tính chất gì?</li></ol>',
    [(r'"Dùng quy ước: $d\'\gt0$ ảnh thật, $d\'\lt0$ ảnh ảo"', r"Quy ước dấu", r"⚠ Công thức thấu kính chỉ đúng khi $f$ và $d'$ mang dấu theo quy ước nào?"),
     (r'"thấu kính hội tụ có tiêu cự $16\ \text{cm}$"', r"$f=+16$ cm", r"Kính hội tụ thì $f$ mang dấu gì?"),
     (r'"$AB$ cao $3\ \text{cm}$"', r"$h=3$ cm", r"$h'$ tính từ đại lượng nào của đề?"),
     (r'"cách thấu kính $24\ \text{cm}$. Tìm vị trí và chiều cao của ảnh"', r"$d=24$ cm", r"$d$ so với $f$ thì ảnh thuộc loại nào? Tìm $d'$ rồi $h'$ theo thứ tự nào?"),
     (r'"cách thấu kính $10\ \text{cm}$ ... (có dấu)"', r"$d=10$ cm", r"Đổi $d$ thì $f$ có đổi không? Dấu của $d'$ lần này cho biết điều gì?")],
    cong_cu_3(),
    [
        dict(tieu_de="Câu a: loại ảnh",
             buoc=dict(hoi="Câu a: vật ngoài hay trong tiêu điểm, ảnh thuộc loại nào?",
                       lua_chon=[(r"Vật ngoài tiêu điểm ($d\gt f$): ảnh thật, $d'\gt0$", True),
                                 (r"Vật trong tiêu điểm ($d\lt f$): ảnh ảo, $d'\lt0$", r"Vật cách kính $24\ \text{cm}$, lớn hơn $f=16\ \text{cm}$, nên vật ở ngoài tiêu điểm."),
                                 (r"Vật đúng tại tiêu điểm: không có ảnh", r"Chỉ không có ảnh khi $d=f$; ở đây $d\ne f$.")],
                       loi="Không so $d$ với $f$ trước, nên không dự đoán được dấu của $d'$ để kiểm tra kết quả."),
             sol=[("p", r"$d=24\ \text{cm}\gt f=16\ \text{cm}$: vật ngoài tiêu điểm nên ảnh thật, $d'\gt0$.")]),
        dict(tieu_de="Câu a: vị trí ảnh",
             buoc=dict(hoi="Câu a: ảnh cách thấu kính bao nhiêu cm?", dap_so=48, don_vi="cm", sai_so=0.5,
                       loi=r"Cộng $\dfrac1f+\dfrac1d$ thay vì trừ, ra $d'=9{,}6\ \text{cm}$ nhỏ hơn $f$, trái với ảnh thật đã nhận ở bước 1.",
                       ke=[(r"Chuyển vế $\dfrac1{d'}=\dfrac1f-\dfrac1d$ rồi lấy nghịch đảo", True),
                           (r"Lấy $d'=f-d$", "Công thức làm việc với nghịch đảo; trừ thẳng hai khoảng cách không cho vị trí ảnh."),
                           (r"Cộng hai nghịch đảo: $\dfrac1{d'}=\dfrac1f+\dfrac1d$", r"Chuyển vế $\dfrac1d$ sang vế kia phải đổi dấu thành phép trừ.")]),
             sol=[("m", r"\dfrac{1}{d'}=\dfrac1f-\dfrac1d"),
                  ("m", r"\dfrac{1}{d'}=\dfrac1{16}-\dfrac1{24}=\dfrac{1}{48}"),
                  ("a", r"d'=48\ \text{cm}"),
                  ("p", r"Kiểm tra: $d'\gt0$ khớp bước 1.")]),
        dict(tieu_de="Câu a: chiều cao ảnh",
             buoc=dict(hoi="Câu a: ảnh cao bao nhiêu cm?", dap_so=6, don_vi="cm", sai_so=0.1,
                       loi=r"Lấy tỉ số ngược $\dfrac{d}{|d'|}$ nên ra ảnh nhỏ hơn vật ($1{,}5\ \text{cm}$).",
                       ke=[(r"$h'=h\cdot\dfrac{|d'|}{d}$", True),
                           (r"$h'=h\cdot\dfrac{d}{|d'|}$", "Tỉ số bị đảo ngược; ảnh thật ở xa kính hơn vật phải lớn hơn vật."),
                           (r"$h'=h\cdot\dfrac{d'}{f}$", r"$\dfrac{d'}{f}$ không phải số phóng đại; $k=\dfrac{|d'|}{d}$.")]),
             sol=[("m", r"k=\dfrac{|d'|}{d}=\dfrac{48}{24}=2"),
                  ("m", r"h'=kh=2\cdot3"),
                  ("a", r"h'=6\ \text{cm}")]),
        dict(tieu_de="Câu b: loại ảnh khi đổi d",
             buoc=dict(hoi="Câu b: vật cách kính 10 cm, ảnh có tính chất gì?",
                       lua_chon=[("Vật trong tiêu điểm: ảnh ảo, cùng chiều, lớn hơn vật", True),
                                 ("Vật trong tiêu điểm: ảnh thật, ngược chiều", "Vật trong $OF$ cho tia ló loe ra, không gặp nhau thật nên không có ảnh thật."),
                                 ("Vật ngoài tiêu điểm: ảnh thật như câu a", r"$d=10\ \text{cm}$ nhỏ hơn $f=16\ \text{cm}$ nên vật đã vào trong tiêu điểm.")],
                       loi="Dùng lại kết luận 'ảnh thật' của câu a, không so lại $d$ mới với $f$.",
                       ke=[(r"Đổi $d$ rồi so lại $d$ với $f$ trước khi tính", True),
                           (r"Dùng luôn $d'$ của câu a vì cùng một thấu kính", r"$d'$ phụ thuộc $d$; đổi $d$ thì ảnh đổi vị trí."),
                           (r"Đổi $f$ thành $10\ \text{cm}$", r"$f$ là đặc trưng của kính, không đổi; cái đổi là $d$.")]),
             sol=[("p", r"$d=10\ \text{cm}\lt f=16\ \text{cm}$: vật trong tiêu điểm nên ảnh ảo, cùng chiều, lớn hơn vật; dự đoán $d'\lt0$.")]),
        dict(tieu_de="Câu b: vị trí ảnh (có dấu)",
             buoc=dict(hoi="Câu b: d′ (có dấu) bằng bao nhiêu cm?", dap_so=-26.7, don_vi="cm", sai_so=0.3,
                       loi=r"Bỏ dấu âm vì cho rằng khoảng cách không thể âm, rồi kết luận ảnh thật.",
                       ke=[(r"Giải $\dfrac1{d'}=\dfrac1f-\dfrac1d$ và giữ nguyên dấu âm của kết quả", True),
                           ("Bỏ dấu âm vì khoảng cách không thể âm", r"Dấu âm của $d'$ cho biết ảnh ảo; bỏ dấu là mất thông tin này (chỉ lấy $|d'|$ khi tính $k$)."),
                           ("Dừng lại vì mẫu số ra âm", r"Mẫu âm vẫn giải được; $d'\lt0$ là kết quả hợp lệ cho ảnh ảo.")]),
             sol=[("m", r"\dfrac{1}{d'}=\dfrac1{16}-\dfrac1{10}=-\dfrac{3}{80}"),
                  ("a", r"d'=-\dfrac{80}{3}\approx-26{,}7\ \text{cm}"),
                  ("p", r"$d'\lt0$: ảnh ảo, nằm cùng phía với vật, khớp bước 4.")]),
        dict(tieu_de="Câu b: chiều cao ảnh",
             buoc=dict(hoi="Câu b: ảnh cao bao nhiêu cm?", dap_so=8, don_vi="cm", sai_so=0.1,
                       loi=r"Dùng $k=\dfrac{d'}{d}$ giữ dấu âm rồi kết luận 'ảnh ngược chiều'; thực ra $d'\lt0$ là ảnh ảo, cùng chiều.",
                       ke=[(r"$k=\dfrac{|d'|}{d}$ với $|d'|$ lấy trị tuyệt đối", True),
                           (r"$k=\dfrac{d'}{d}$ giữ dấu âm rồi kết luận ảnh ngược chiều", r"Dấu âm của $d'$ báo ảnh ảo (cùng chiều), không phải 'ngược chiều'; số phóng đại viết theo $|d'|$."),
                           (r"$k=\dfrac fd$", r"$\dfrac fd$ không phải số phóng đại; $k=\dfrac{|d'|}{d}$.")]),
             sol=[("m", r"k=\dfrac{|d'|}{d}=\dfrac{80/3}{10}=\dfrac83"),
                  ("m", r"h'=kh=\dfrac83\cdot3"),
                  ("a", r"h'=8\ \text{cm}")]),
    ],
    [r"<b>Công thức thấu kính</b>: $\dfrac1f=\dfrac1d+\dfrac1{d'}$; $f\gt0$ hội tụ, $f\lt0$ phân kì; $d\gt0$.",
     r"<b>Dấu của $d'$</b>: $d'\gt0$ ảnh thật; $d'\lt0$ ảnh ảo (cùng phía vật).",
     r"<b>Số phóng đại</b>: $k=\dfrac{h'}{h}=\dfrac{|d'|}{d}$; $k\gt1$ ảnh lớn hơn vật.",
     "Cùng đơn vị độ dài cho $f$, $d$, $d'$."],
    [r"a) $d'=48\ \text{cm}$ (ảnh thật), $h'=6\ \text{cm}$", r"b) $d'\approx-26{,}7\ \text{cm}$ (ảnh ảo, cùng chiều, lớn hơn vật), $h'=8\ \text{cm}$"],
    r"Dạng này nhận ra khi: đề cho $f$, $d$, $h$ → so $d$ với $f$ để đoán loại ảnh, tìm $d'$ bằng nghịch đảo, rồi $k=\dfrac{|d'|}{d}$.",
    4)

# ───────── Dạng 4 ─────────
D4 = dang(
    "Dạng 4 · Khó · Bài ngược: biết d và độ cao ảnh, tìm loại kính, d′ và f", T88, "bai_tap", 3, "giau_tu_buoc_2",
    r"Thấy <b>cho độ cao ảnh, ảnh ảo nhỏ hơn vật</b> → <b>phân kì</b>; tìm <b>$|d'|=kd$</b> rồi <b>$f$ có dấu</b>",
    {"cho": [r"vật $AB=6$ cm, $d=36$ cm", r"ảnh ảo cao $2$ cm", "kính L chưa biết loại"],
     "tim": ["a) loại kính L", r"b) $d'$ (có dấu), $f$ (có dấu)", r"c) ảnh có nằm trong khoảng $OF'$ không?"]},
    r"<p>Vật sáng $AB$ cao $6\ \text{cm}$ đặt vuông góc với trục chính của thấu kính $L$ (chưa biết loại), $A$ nằm trên trục chính và cách $L$ một đoạn $36\ \text{cm}$. "
    r"Ảnh $A'B'$ của $AB$ qua $L$ là ảnh ảo, cao $2\ \text{cm}$.</p>"
    r'<ol type="a"><li>$L$ là thấu kính loại nào? Giải thích.</li>'
    r"<li>Tìm vị trí ảnh $d'$ (có dấu) và tiêu cự $f$ (có dấu) của $L$.</li>"
    r"<li>Ảnh có nằm trong khoảng $OF'$ không?</li></ol>",
    [(r'"thấu kính $L$ (chưa biết loại)"', r"Cần xác định loại", r"Hai loại kính cho ảnh ảo khác nhau ở điểm nào về độ lớn so với vật?"),
     (r'"$AB$ cao $6\ \text{cm}$ ... cách $L$ $36\ \text{cm}$"', r"$h=6$ cm; $d=36$ cm", r"⚠ Vật có phải vật thật không? $d$ mang dấu gì?"),
     (r'"ảnh ảo, cao $2\ \text{cm}$"', r"$h'=2$ cm; ảnh ảo nên $d'\lt0$", r"Từ $h'$ và $h$ suy ra đại lượng nào? Độ lớn của $d'$ lấy từ đâu?"),
     (r'"Tìm ... tiêu cự $f$ (có dấu)"', r"Đã có $d$ và $d'$", r"Thế $d$ và $d'$ có dấu vào công thức nào để ra $f$?"),
     (r'"Ảnh có nằm trong khoảng $OF\'$ không?"', r"So $|d'|$ với $|f|$", r"Hai độ dài nào cần so sánh?")],
    cong_cu_4(),
    [
        dict(tieu_de="Nhận ra loại kính",
             buoc=dict(hoi="Thấu kính L thuộc loại nào?",
                       lua_chon=[("Phân kì: ảnh ảo nhỏ hơn vật", True),
                                 ("Hội tụ: vật ngoài tiêu điểm cho ảnh ảo", r"Kính hội tụ cho ảnh ảo chỉ khi vật trong $OF$, và khi đó ảnh lớn hơn vật."),
                                 ("Chưa kết luận được khi chưa biết $f$", "Tính chất ảnh (ảo và nhỏ hơn vật) đã đủ để phân biệt hai loại kính.")],
                       loi="Thấy 'ảnh ảo' nên nghĩ ngay kính hội tụ (kính lúp), bỏ qua dữ kiện ảnh nhỏ hơn vật."),
             sol=[("p", "Ảnh ảo <b>nhỏ hơn</b> vật ($2\\ \\text{cm}\\lt6\\ \\text{cm}$). Kính hội tụ cho ảnh ảo thì ảnh lớn hơn vật, nên $L$ là kính phân kì, $f\\lt0$."),
                  ("a", "T:Thấu kính phân kì.")]),
        dict(tieu_de="Vị trí ảnh",
             buoc=dict(hoi="d′ (có dấu) bằng bao nhiêu cm?", dap_so=-12, don_vi="cm", sai_so=0.3,
                       loi=r"Tính đúng độ lớn nhưng lấy $d'$ dương vì là khoảng cách, nên mất thông tin ảnh ảo.",
                       ke=[(r"Từ $k=\dfrac{|d'|}{d}$ tính $|d'|$, rồi gán dấu âm vì ảnh ảo", True),
                           (r"Tính $|d'|$ từ $k$ rồi lấy $d'$ dương vì là khoảng cách", r"Ảnh ảo thì $d'\lt0$; $|d'|$ chỉ là độ lớn."),
                           (r"Thế vào $\dfrac1f=\dfrac1d+\dfrac1{d'}$ ngay", r"Công thức có hai ẩn $f$ và $d'$; cần tìm $d'$ từ $k$ trước.")]),
             sol=[("m", r"k=\dfrac{h'}{h}=\dfrac26=\dfrac13"),
                  ("m", r"|d'|=k\,d=\dfrac13\cdot36"),
                  ("p", r"Ảnh ảo nên $d'\lt0$."),
                  ("a", r"d'=-12\ \text{cm}")]),
        dict(tieu_de="Tiêu cự có dấu",
             buoc=dict(hoi="Tiêu cự f (có dấu) bằng bao nhiêu cm?", dap_so=-18, don_vi="cm", sai_so=0.5,
                       loi=r"Thế $d'=+12$ (bỏ dấu âm) nên ra $f=+9\ \text{cm}$, trái với loại kính đã nhận ở bước 1.",
                       ke=[(r"Thế $d$ và $d'$ có dấu vào $\dfrac1f=\dfrac1d+\dfrac1{d'}$", True),
                           (r"Thế $d'$ dương vì là khoảng cách", r"Ảnh ảo phải thế $d'\lt0$; thế dương cho $f\gt0$, mâu thuẫn với kính phân kì."),
                           (r"Dùng $f=\dfrac{d\,d'}{d-d'}$", r"Quy đồng $\dfrac1f=\dfrac1d+\dfrac1{d'}$ cho $f=\dfrac{d\,d'}{d+d'}$ (cộng, không trừ).")]),
             sol=[("m", r"\dfrac1f=\dfrac1d+\dfrac1{d'}=\dfrac1{36}-\dfrac1{12}=-\dfrac1{18}"),
                  ("a", r"f=-18\ \text{cm}"),
                  ("p", "Kiểm tra: $f\\lt0$ khớp kính phân kì.")]),
        dict(tieu_de="Kiểm tra vị trí ảnh",
             buoc=dict(hoi="Ảnh A′B′ có nằm trong khoảng OF′ không?",
                       lua_chon=[(r"Có, vì $|d'|\lt|f|$", True),
                                 (r"Không, vì ảnh ảo luôn nằm ngoài tiêu điểm", r"Với kính phân kì, ảnh ảo của vật thật luôn nằm giữa $O$ và $F'$."),
                                 ("Không kiểm tra được vì $f$ âm", r"So sánh độ dài $|d'|$ với $|f|$; dấu chỉ để nhận loại ảnh và loại kính.")],
                       loi=r"So sánh $d'$ với $f$ khi còn mang dấu âm, nên cho rằng $-12\lt-18$ là sai.",
                       ke=[(r"So hai độ dài $|d'|$ và $|f|$", True),
                           (r"So thẳng $d'$ với $f$ cùng dấu âm", r"Khi còn dấu âm, số nào lớn hơn dễ nhầm; vị trí trên trục được so bằng độ dài."),
                           (r"Dựa vào dấu của $f$ để kết luận", r"Dấu của $f$ chỉ cho biết loại kính, không cho biết ảnh nằm trong hay ngoài $OF'$.")]),
             sol=[("p", r"$|d'|=12\ \text{cm}\lt|f|=18\ \text{cm}$: ảnh nằm giữa $O$ và $F'$, khớp tính chất ảnh qua kính phân kì."),
                  ("a", "T:Có.")]),
    ],
    [r"<b>Số phóng đại</b>: $k=\dfrac{h'}{h}=\dfrac{|d'|}{d}$.",
     r"<b>Loại kính theo ảnh</b>: ảnh ảo nhỏ hơn vật là kính phân kì ($f\lt0$); ảnh ảo lớn hơn vật là kính hội tụ.",
     r"<b>Dấu</b>: $d'\lt0$ ảnh ảo. Công thức $\dfrac1f=\dfrac1d+\dfrac1{d'}$ phải thế đúng dấu."],
    ["a) Thấu kính phân kì", r"b) $d'=-12\ \text{cm}$; $f=-18\ \text{cm}$", r"c) Có, vì $|d'|\lt|f|$"],
    r"Dạng này nhận ra khi: đề cho độ cao ảnh (hoặc 'nhỏ hơn/lớn hơn vật') và tính chất ảnh → $|d'|=kd$ trước, gán dấu theo ảnh thật/ảo, rồi mới tìm $f$.",
    2)

# ───────── Dạng 5 ─────────
D5 = dang(
    "Dạng 5 · Nâng cao · Kết hợp: tìm vị trí vật cho ảnh cho trước, rồi vật dịch chuyển", T88, "bai_tap", 4, "giau_het",
    r"Thấy <b>ảnh rõ trên màn cao gấp k lần, rồi vật dịch</b> → <b>$d'=kd$</b> cho vị trí đầu; mỗi vị trí mới <b>tính lại $d'$</b>",
    {"cho": [r"hội tụ $f=18$ cm; $AB=1{,}5$ cm", r"ảnh thật trên màn, cao gấp $3$ lần vật (vị trí $P$)", r"từ $P$ dịch vật ra xa $6$ cm"],
     "tim": [r"a) $d$, $d'$ tại $P$", r"b) màn dịch bao nhiêu cm, chiều nào; chiều cao ảnh mới"]},
    r"<p>Thấu kính hội tụ có tiêu cự $18\ \text{cm}$. Vật sáng $AB$ cao $1{,}5\ \text{cm}$ đặt vuông góc với trục chính, $A$ nằm trên trục chính. "
    r"Đưa $AB$ từ rất xa lại gần thấu kính cho tới vị trí $P$ mà ảnh $A'B'$ hiện rõ trên màn và cao gấp $3$ lần vật.</p>"
    r'<ol type="a"><li>Khi vật ở $P$, vật và màn cách thấu kính bao nhiêu cm?</li>'
    r"<li>Từ $P$, dịch $AB$ ra xa thấu kính thêm $6\ \text{cm}$. Phải dịch màn đi bao nhiêu cm, về phía nào, để lại thu được ảnh rõ? Ảnh khi đó cao bao nhiêu?</li></ol>",
    [(r'"thấu kính hội tụ có tiêu cự $18\ \text{cm}$"', r"$f=+18$ cm", r"⚠ Quy ước dấu của $f$, $d$, $d'$ dùng thống nhất cho cả hai vị trí vật không?"),
     (r'"$AB$ cao $1{,}5\ \text{cm}$"', r"$h=1{,}5$ cm", r"Chiều cao ảnh tính từ đại lượng nào?"),
     (r'"ảnh $A\'B\'$ hiện rõ trên màn"', r"ảnh thật, $d'\gt0$", r"Ảnh hứng được trên màn là ảnh loại nào?"),
     (r'"cao gấp $3$ lần vật"', r"$k=3$", r"Từ $k$ viết được hệ thức nào giữa $d'$ và $d$?"),
     (r'"dịch $AB$ ra xa thấu kính thêm $6\ \text{cm}$"', r"$d_2=d+6$", r"Khoảng cách mới là bao nhiêu? $d'$ cũ còn dùng được không?"),
     (r'"Phải dịch màn đi bao nhiêu cm, về phía nào"', r"So $d_2'$ với $d'$", r"Ảnh thật dịch lại gần hay ra xa kính khi vật ra xa?")],
    cong_cu_5(),
    [
        dict(tieu_de="Hệ thức giữa d′ và d tại P",
             buoc=dict(hoi="Điều kiện 'ảnh rõ trên màn, cao gấp 3 lần vật' cho hệ thức nào?",
                       lua_chon=[(r"Ảnh thật nên $d'\gt0$ và $d'=3d$", True),
                                 (r"$d'=-3d$ vì ảnh lớn hơn vật", r"Ảnh hứng được trên màn là ảnh thật, $d'\gt0$; ảnh ảo mới có $d'\lt0$."),
                                 (r"$d'=\dfrac d3$ vì $k=3$", r"$k=\dfrac{|d'|}{d}$ nên $|d'|=kd$, không phải $\dfrac d3$.")],
                       loi="Thấy 'lớn gấp 3' nên chọn dấu âm hoặc chia cho 3, không dùng $k=|d'|/d$."),
             sol=[("p", "Hứng được trên màn là ảnh thật, nên $d'\\gt0$."),
                  ("m", r"k=\dfrac{d'}{d}=3\ \Rightarrow\ d'=3d"),
                  ("a", "T:$d'=3d$.")]),
        dict(tieu_de="Vị trí vật P",
             buoc=dict(hoi="Ở vị trí P, vật cách thấu kính bao nhiêu cm?", dap_so=24, don_vi="cm", sai_so=0.3,
                       loi=r"Dùng $d=f(1+3)$: đó là công thức của $d'$, không phải $d$; hoặc lấy $d=\dfrac f3$.",
                       ke=[(r"Thế $d'=3d$ vào $\dfrac1f=\dfrac1d+\dfrac1{d'}$ rồi giải ra $d$", True),
                           (r"Lấy $d=f\,(1+3)$", r"$f(1+k)$ cho vị trí ảnh $d'$, không phải vị trí vật; từ $d'=3d$ phải giải ra $d$."),
                           (r"Lấy $d=\dfrac f3$ vì ảnh gấp $3$ lần", r"Số $3$ là tỉ số $\dfrac{|d'|}{d}$, không phải $\dfrac fd$.")]),
             sol=[("m", r"\dfrac1f=\dfrac1d+\dfrac1{3d}=\dfrac{4}{3d}"),
                  ("m", r"d=\dfrac{4f}{3}=\dfrac{4\cdot18}{3}"),
                  ("a", r"d=24\ \text{cm}")]),
        dict(tieu_de="Vị trí màn",
             buoc=dict(hoi="Màn cách thấu kính bao nhiêu cm?", dap_so=72, don_vi="cm", sai_so=1,
                       loi=r"Tính $\dfrac1f-\dfrac1d$ rồi lấy luôn kết quả làm $d'$, quên lấy nghịch đảo.",
                       ke=[(r"Dùng hệ thức đã có $d'=3d$", True),
                           (r"Tính $\dfrac1f-\dfrac1d$ rồi lấy kết quả làm $d'$", r"Hiệu đó là $\dfrac1{d'}$; phải lấy nghịch đảo."),
                           (r"Lấy $d'=d+f$", "Tổng hai khoảng cách không cho vị trí ảnh; phải dùng công thức thấu kính hoặc $d'=3d$.")]),
             sol=[("m", r"d'=3d=3\cdot24"),
                  ("a", r"d'=72\ \text{cm}"),
                  ("p", r"Kiểm tra: $\dfrac1{24}+\dfrac1{72}=\dfrac{4}{72}=\dfrac1{18}$ đúng; $h'=3\cdot1{,}5=4{,}5\ \text{cm}$.")]),
        dict(tieu_de="Khoảng cách vật sau khi dịch",
             buoc=dict(hoi="Sau khi dịch ra xa 6 cm, vật cách thấu kính bao nhiêu cm?", dap_so=30, don_vi="cm", sai_so=0.2,
                       loi="Lấy hiệu thay vì tổng, hoặc lấy $d_2=6$ (quãng đường dịch) làm khoảng cách mới.",
                       ke=[(r"$d_2=d+6$ vì dịch ra xa thì khoảng cách tăng", True),
                           (r"$d_2=d-6$", "Dịch ra xa nghĩa là khoảng cách tăng, không giảm."),
                           (r"$d_2=6$", r"$6\ \text{cm}$ là quãng đường dịch thêm, không phải khoảng cách mới tới thấu kính.")]),
             sol=[("m", r"d_2=d+6"),
                  ("a", r"d_2=30\ \text{cm}")]),
        dict(tieu_de="Ảnh mới ở đâu",
             buoc=dict(hoi="Ảnh mới cách thấu kính bao nhiêu cm?", dap_so=45, don_vi="cm", sai_so=0.5,
                       loi=r"Giữ $d'=3d$ như ở P, hoặc cộng $d'+6$ vì tưởng ảnh dịch cùng quãng với vật.",
                       ke=[(r"Giải lại $\dfrac1{d_2'}=\dfrac1f-\dfrac1{d_2}$ với $d_2$ mới", True),
                           (r"Giữ $d'=3d_2$ như ở P", r"Hệ thức $d'=3d$ chỉ đúng ở P; khi vật dịch thì $k$ đã đổi."),
                           (r"Cộng $d_2'=d'+6$", "Ảnh không dịch cùng quãng và cùng chiều với vật; phải tính lại bằng công thức thấu kính.")]),
             sol=[("m", r"\dfrac1{d_2'}=\dfrac1f-\dfrac1{d_2}=\dfrac1{18}-\dfrac1{30}=\dfrac1{45}"),
                  ("a", r"d_2'=45\ \text{cm}")]),
        dict(tieu_de="Chiều dịch của màn",
             buoc=dict(hoi="Màn phải dịch về phía nào so với thấu kính?",
                       lua_chon=[("Lại gần thấu kính", True),
                                 ("Ra xa thấu kính", "Vật ra xa thấu kính thì ảnh thật lại gần kính hơn; so $d_2'$ với $d'$ sẽ thấy ảnh gần kính hơn."),
                                 ("Không cần dịch", "Ảnh đã đổi vị trí, màn đứng yên thì ảnh trên màn bị nhòe.")],
                       loi="Nghĩ vật ra xa thì ảnh cũng ra xa theo, giống chuyển động của vật.",
                       ke=[("So vị trí ảnh mới với vị trí ảnh cũ", True),
                           ("Cho rằng ảnh dịch cùng chiều với vật", "Ảnh thật dịch ngược lại: vật ra xa thì ảnh lại gần kính."),
                           ("Chỉ dựa vào $d$ tăng mà kết luận ngay", "Phải so $d_2'$ với $d'$ đã tính, không đoán theo chiều dịch của vật.")]),
             sol=[("p", r"$d_2'=45\ \text{cm}\lt d'=72\ \text{cm}$: ảnh thật lại gần thấu kính hơn."),
                  ("a", "T:Dịch màn lại gần thấu kính.")]),
        dict(tieu_de="Màn dịch bao nhiêu",
             buoc=dict(hoi="Màn phải dịch một đoạn bao nhiêu cm?", dap_so=27, don_vi="cm", sai_so=0.5,
                       loi="Lấy độ dịch của màn bằng độ dịch của vật ($6$ cm).",
                       ke=[(r"Lấy hiệu hai vị trí ảnh $d'-d_2'$", True),
                           ("Lấy độ dịch của vật làm độ dịch của màn", "Ảnh không dịch cùng quãng với vật; độ dịch của màn là hiệu hai vị trí ảnh."),
                           (r"Lấy tổng $d'+d_2'$", "Tổng hai khoảng cách tới kính không phải độ dịch; màn đi từ vị trí này sang vị trí kia.")]),
             sol=[("m", r"\Delta=d'-d_2'=72-45"),
                  ("a", r"\Delta=27\ \text{cm (lại gần thấu kính)}")]),
        dict(tieu_de="Chiều cao ảnh mới",
             buoc=dict(hoi="Ảnh mới cao bao nhiêu cm?", dap_so=2.25, don_vi="cm", sai_so=0.05,
                       loi="Giữ $k=3$ như ở P nên ra ảnh cao 4,5 cm; số phóng đại đã đổi khi vật dịch.",
                       ke=[(r"Tính lại $k=\dfrac{d_2'}{d_2}$ rồi $h_2'=kh$", True),
                           (r"Giữ $k=3$ như ở P", "Số phóng đại phụ thuộc vị trí vật; vật dịch thì $k$ đổi."),
                           (r"Lấy $h_2'=h\cdot\dfrac{d_2}{d_2'}$", "Tỉ số bị đảo ngược; ảnh thật ở xa kính hơn vật mới lớn hơn vật.")]),
             sol=[("m", r"k_2=\dfrac{d_2'}{d_2}=\dfrac{45}{30}=1{,}5"),
                  ("m", r"h_2'=k_2h=1{,}5\cdot1{,}5"),
                  ("a", r"h_2'=2{,}25\ \text{cm}"),
                  ("p", r"Kiểm tra: vật ra xa nên ảnh nhỏ đi ($4{,}5\to2{,}25\ \text{cm}$). Hợp lí.")]),
    ],
    [r"<b>Ảnh thật</b> hứng được trên màn: $d'\gt0$. <b>Số phóng đại</b> $k=\dfrac{|d'|}{d}$.",
     r"<b>Công thức thấu kính</b>: $\dfrac1f=\dfrac1d+\dfrac1{d'}$ — dùng riêng cho từng vị trí vật.",
     r"<b>Vật xa kính hơn</b> thì ảnh thật gần kính hơn và nhỏ hơn."],
    [r"a) $d=24\ \text{cm}$; màn cách kính $72\ \text{cm}$", r"b) Dịch màn lại gần kính $27\ \text{cm}$; ảnh cao $2{,}25\ \text{cm}$"],
    r"Dạng này nhận ra khi: đề cho tỉ số ảnh/vật rồi dịch vật → dùng $d'=kd$ cho vị trí đầu; mỗi vị trí mới phải tính lại $d'$ và $k$.",
    1)


def main():
    kiem_so()
    dang_bai = [D1, D2, D3, D4, D5]
    d = {"lesson_id": 86, "lesson_title": "Bài 8. Thấu kính", "generated_at": "2026-11-10",
         "review": {"checked": False, "notes": "chờ kiểm chéo"}, "dang_bai": dang_bai}
    out = os.path.join(HERE, "86.json")
    # chuỗi raw r'...\'...' giữ nguyên dấu gạch chéo → KaTeX hiểu \' là dấu sắc; bỏ gạch chéo trước dấu nháy
    text = json.dumps(d, ensure_ascii=False, indent=1).replace("\\\\'", "'")
    open(out, "w").write(text + "\n")
    print("ghi", out, len(dang_bai), "dạng")


if __name__ == "__main__":
    main()
