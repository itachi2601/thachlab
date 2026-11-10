"""Bài tập mẫu bài 88 "Bài 10. Kính lúp. Bài tập thấu kính" (KHTN 9) — lesson_id 88. Chuẩn "một dạng — một hình":
hình duy nhất = cong_cu (họ thau_kinh, de:true), không còn <figure> trong problem_html / analysis_html.
Quy ước dấu (lý thuyết bài 88, nhắc lại từ Bài 8): 1/f = 1/d + 1/d' ; f > 0 (chỉ thấu kính hội tụ) ; d' > 0 ảnh thật,
d' < 0 ảnh ảo cùng phía vật ; k = h'/h = |d'|/d ; G = 25/f (f tính bằng cm), G ứng với ảnh ở rất xa nên khác k.
Bài 88 không có chủ đề ngân hàng riêng → dùng chủ đề của bài 86 "Công thức thấu kính và số phóng đại"
(D1–D3 form ly_thuyet vì chủ đề chỉ có 4 câu bai_tap; D4 form bai_tap). Chủ đề kính lúp (G = 25/f) chưa có trong ngân hàng.
Chạy: python3 scripts/data/bai-tap-mau/build-hinh-88.py   (idempotent; không ghi DB). Không ghi review.checked=true."""
import json, os, re, sys
from fractions import Fraction as F
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "../../../.claude/skills/soan-bai-tap-mau/scripts"))
from dung import write, inject, sol, buoc, M, P, A

J = os.path.join(HERE, "88.json")
TOPIC = "Công thức thấu kính và số phóng đại"


def anh(f, d):
    """d' theo 1/f = 1/d + 1/d' (Fraction)."""
    return 1 / (1 / F(f) - 1 / F(d))


# ═════════════ SỐ LIỆU (đáp số tính ở đây, assert kiểm lại) ═════════════
# D1 — kính 2x (f = 12,5), hoa cách kính 7,5 cm; kính thứ hai ghi 5x
G1 = F(2); f1 = 25 / G1; d1 = F("7.5"); dp1 = anh(f1, d1); f1b = 25 / F(5)
assert (f1, dp1, f1b, f1 - f1b) == (F("12.5"), F("-18.75"), 5, F("7.5")) and abs(dp1) / d1 == F("2.5") and d1 < f1
# D2 — kính 12,5x (f = 2), ảnh ảo cách kính 6 cm, kiến cao 1,5 mm
G2 = F("12.5"); f2 = 25 / G2; dp2 = F(-6); h2 = F("1.5")
d2 = 1 / (1 / f2 - 1 / dp2); k2 = abs(dp2) / d2; hp2 = k2 * h2
assert (f2, d2, k2, hp2) == (2, F("1.5"), 4, 6) and anh(f2, d2) == dp2 and k2 != G2
assert 1 / (1 / f2 - F(1, 6)) == 3                       # thế nhầm d' = +6 → d = 3
# D3 — kính 5x (f = 5), đầu đinh ghim cao 2 mm cách kính 3 cm, nâng thêm 1,5 cm
G3 = F(5); f3 = 25 / G3; d3a = F(3); d3b = d3a + F("1.5"); h3 = F(2)
dp3a, dp3b = anh(f3, d3a), anh(f3, d3b)
k3a, k3b = abs(dp3a) / d3a, abs(dp3b) / d3b
assert (f3, dp3a, dp3b, k3a, k3b) == (5, F("-7.5"), -45, F("2.5"), 10) and k3a * h3 == 5 and k3b * h3 == 20 and f3 - d3b == F("0.5")
assert k3a != G3 and k3b != G3 and G3 * h3 == 10         # k ≠ G ở cả hai vị trí
assert F(1, 3) - F(2, 15) == F(1, 5) and F(2, 9) - F(1, 45) == F(1, 5)
# D4 — thấu kính f = 9, vật 2 cm, ảnh 6 cm (k = 3) → ảnh thật d = 12, ảnh ảo d = 6
f4 = F(9); h4, hp4 = F(2), F(6); k4 = hp4 / h4
d4t = f4 * (k4 + 1) / k4; d4a = f4 * (k4 - 1) / k4
assert (k4, d4t, d4a) == (3, 12, 6) and anh(f4, d4t) == 36 and anh(f4, d4a) == -18 and d4a < f4 < d4t
assert (F(1, 9) == F(1, 12) + F(1, 36)) and (F(1, 9) == F(1, 6) - F(1, 18))


# ═════════════ Hình (cong_cu thau_kinh) ═════════════
def n(x):
    return float(x) if not isinstance(x, (int, float)) else x


def tia_ao(d, h, f, x_phai, x_trai=None):
    """Hai tia từ B (vật trong tiêu cự): ló loe ra + đường kéo dài nét đứt tới B' (x_trai = cắt ở mép khung)."""
    d, h, f = n(d), n(h), n(f)
    dp = d * f / (f - d)                                   # |d'|
    xt = -dp if x_trai is None else x_trai
    y1 = lambda x: h * (1 - x / f)                         # tia song song → qua F'
    y2 = lambda x: -h * x / d                              # tia qua O
    return [
        {"loai": "tia", "qua": [[-d, h], [0, h], [x_phai, round(y1(x_phai), 4)]], "keo": [[0, h], [xt, round(y1(xt), 4)]], "mau": "max"},
        {"loai": "tia", "qua": [[-d, h], [0, 0]], "keo": [[-d, h], [xt, round(y2(xt), 4)]], "mep": True},
    ]


def tia_thuc(d, h, f):
    d, h, f = n(d), n(h), n(f)
    dp = d * f / (d - f); hp = -h * dp / d
    return [
        {"loai": "tia", "qua": [[-d, h], [0, h], [dp, hp]], "mau": "max"},
        {"loai": "tia", "qua": [[-d, h], [0, 0], [dp, hp]], "mau": "min"},
    ]


TK_F = lambda f: {"loai": "tk", "x": 0, "kieu": "hoi_tu", "f": f, "vi_tieu": ["b", "b"]}
VAT = lambda x, h: {"loai": "vat", "x": x, "h": h, "ten": ["A", "B"]}
ANH_AO = lambda x, h: {"loai": "vat", "x": x, "h": h, "ao": True, "ten": ["", "B′"], "mau": "max"}


def S(x_min, x_max, pd=1):
    """đơn vị hình (ngang 20) trên mỗi cm theo trục đứng — để đặt thước/nhãn theo đơn vị hình, tránh đè nhãn."""
    return 20 / (x_max - x_min) * pd


def cc_d1():
    f, d, dp = 12.5, 7.5, 18.75
    X0, X1, PD = -22, 16, 2
    s = S(X0, X1, PD)
    TKV = {"loai": "tk", "x": 0, "kieu": "hoi_tu", "f": f, "vi_tieu": ["l", "b"]}
    return {"loai": "thau_kinh", "de": True,
            "phan": [{"tu_buoc": 0, "x_min": X0, "x_max": X1, "y_tren": 4.0, "y_duoi": round(-3.3 / s, 2), "phong_doc": PD, "hinh": [
                {"loai": "tk", "x": 0, "kieu": "hoi_tu", "ten": "2×"},
                VAT(-d, 1),
                {"loai": "thuoc", "tu": -d, "den": 0, "o": round(-1.9 / s, 2), "nhan": "7,5 cm", "ben": "duoi"}]}],
            "lop": [
                [TKV, {"loai": "ghi", "text": "f = 25 : G = 25 : 2 = 12,5 cm"}],
                tia_ao(d, 1, f, 16) + [ANH_AO(-dp, 2.5), {"loai": "ghi", "text": "d = 7,5 cm < f = 12,5 cm: ảnh ảo, cùng chiều, lớn hơn"}],
                [{"loai": "ghi", "text": "kính 5×: f₂ = 25 : 5 = 5 cm ⇒ ngắn hơn 12,5 − 5 = 7,5 cm"}],
                [{"loai": "ghi", "text": "d′ = −18,75 cm · k = 2,5 (khác G = 2)"}],
            ]}


def cc_d2():
    f, d, h = 2, 1.5, 0.15
    X0, X1, PD = -11, 5, 4
    s = S(X0, X1, PD)
    TKV = {"loai": "tk", "x": 0, "kieu": "hoi_tu", "f": f, "vi_tieu": ["l", "b"]}
    return {"loai": "thau_kinh", "de": True,
            "phan": [{"tu_buoc": 0, "x_min": X0, "x_max": X1, "y_tren": 0.95, "y_duoi": round(-4.9 / s, 2), "phong_doc": PD, "hinh": [
                {"loai": "tk", "x": 0, "kieu": "hoi_tu", "ten": "12,5×"},
                {"loai": "diem", "x": -6, "ten": "A′", "vi": "b"},
                {"loai": "thuoc", "tu": -6, "den": 0, "o": round(-3.5 / s, 3), "nhan": "6 cm", "ben": "duoi"}]}],
            "lop": [
                [TKV, {"loai": "ghi", "text": "f = 25 : 12,5 = 2 cm"}],
                [VAT(-d, h), {"loai": "thuoc", "tu": -d, "den": 0, "o": round(-1.9 / s, 3), "nhan": "1,5 cm", "ben": "duoi"},
                 {"loai": "ghi", "text": "d′ = −6 cm ⇒ 1/d = 1/2 + 1/6 ⇒ d = 1,5 cm"}],
                tia_ao(d, h, f, 5) + [ANH_AO(-6, 0.6), {"loai": "ghi", "text": "k = |d′| : d = 6 : 1,5 = 4 lần"}],
                [{"loai": "thuoc", "tu": 0, "den": 0.6, "o": -7.6, "doc": True, "nhan": "6 mm", "ben": "trai"},
                 {"loai": "ghi", "text": "h′ = k·h = 4·1,5 = 6 mm"}],
                [{"loai": "ghi", "text": "1/2 = 1/1,5 − 1/6 ✓ · k = 4 khác G = 12,5"}],
            ]}


def cc_d3():
    f, d1_, d2_, h = 5, 3, 4.5, 0.2
    A0, A1, B0, B1, PD = -10, 6, -12, 6, 8
    sa, sb = S(A0, A1, PD), S(B0, B1, PD)
    TKV = {"loai": "tk", "x": 0, "kieu": "hoi_tu", "f": f, "vi_tieu": ["l", "b"]}
    return {"loai": "thau_kinh", "de": True,
            "phan": [
                {"tu_buoc": 0, "x_min": A0, "x_max": A1, "y_tren": 1.1, "y_duoi": round(-3.25 / sa, 2), "phong_doc": PD, "hinh": [
                    {"loai": "tk", "x": 0, "kieu": "hoi_tu", "ten": "5×"},
                    VAT(-d1_, h),
                    {"loai": "thuoc", "tu": -d1_, "den": 0, "o": round(-1.9 / sa, 3), "nhan": "3 cm", "ben": "duoi"},
                    {"loai": "chu", "x": -0.6, "y": 0.9, "text": "nâng thêm 1,5 cm", "a": "end"}]},
                {"tu_buoc": 2, "x_min": B0, "x_max": B1, "y_tren": 1.05, "y_duoi": round(-4.85 / sb, 2), "phong_doc": PD, "hinh": [
                    TKV, VAT(-d2_, h),
                    {"loai": "thuoc", "tu": -d2_, "den": 0, "o": round(-1.9 / sb, 3), "nhan": "4,5 cm", "ben": "duoi"}]}],
            "lop": [
                [TKV, {"loai": "ghi", "text": "f = 25 : 5 = 5 cm"}],
                tia_ao(d1_, h, f, 5) + [ANH_AO(-7.5, 0.5), {"loai": "ghi", "text": "d′ = −7,5 cm · k = 7,5 : 3 = 2,5 ⇒ h′ = 5 mm"}],
                tia_ao(d2_, h, f, 6, -12) + [{"loai": "chu", "x": -11.5, "y": 0.9, "text": "ảnh ảo ở xa 45 cm", "a": "start", "mau": "max"},
                                             {"loai": "ghi", "text": "d = 3 + 1,5 = 4,5 cm ⇒ d′ = −45 cm"}],
                [{"loai": "ghi", "text": "k = 45 : 4,5 = 10 ⇒ h′ = 10·2 = 20 mm"}],
                [{"loai": "thuoc", "tu": -d2_, "den": -f, "o": round(-3.5 / sb, 3), "nhan": "0,5 cm", "ben": "duoi"},
                 {"loai": "ghi", "text": "d < f = 5 cm: nâng thêm tối đa 0,5 cm"}],
                [{"loai": "ghi", "text": "1/3 − 2/15 = 1/5 ; 1/4,5 − 1/45 = 1/5 ✓"}],
            ]}


def cc_d4():
    f, h = 9, 2
    a0, a1, pa = -16, 42, 2
    b0, b1 = -24, 16
    sa, sb = S(a0, a1, pa), S(b0, b1)
    G1 = [{"loai": "chu", "x": 41, "y": 7.5, "text": "vật cao 2 cm", "a": "end"}, {"loai": "chu", "x": 41, "y": 5.1, "text": "ảnh cao 6 cm", "a": "end"}]
    G2 = [{"loai": "chu", "x": 15.5, "y": 8.8, "text": "vật cao 2 cm", "a": "end"}, {"loai": "chu", "x": 15.5, "y": 5.6, "text": "ảnh cao 6 cm", "a": "end"}]
    return {"loai": "thau_kinh", "de": True,
            "phan": [
                {"tu_buoc": 0, "x_min": a0, "x_max": a1, "y_tren": 9.5, "y_duoi": -8.1, "phong_doc": pa, "hinh": [{"loai": "tk", "x": 0, "kieu": "hoi_tu", "f": f, "vi_tieu": ["t", "b"]}] + G1},
                {"tu_buoc": 3, "x_min": b0, "x_max": b1, "y_tren": 11.5, "y_duoi": -6.5, "hinh": [TK_F(f)] + G2}],
            "lop": [
                [{"loai": "ghi", "text": "k = h′ : h = 6 : 2 = 3"}],
                [VAT(-12, h), {"loai": "thuoc", "tu": -12, "den": 0, "o": round(-1.9 / sa, 2), "nhan": "12 cm", "ben": "duoi"},
                 {"loai": "ghi", "text": "d′ = 3d ⇒ 1/9 = 4/(3d) ⇒ d = 12 cm"}],
                tia_thuc(12, h, f) + [{"loai": "vat", "x": 36, "h": -6, "ten": ["A′", "B′"], "mau": "max"},
                                      {"loai": "ghi", "text": "d′ = 3d = 36 cm: đặt màn ở đây"}],
                [VAT(-6, h), {"loai": "thuoc", "tu": -6, "den": 0, "o": round(-1.9 / sb, 2), "nhan": "6 cm", "ben": "duoi"},
                 {"loai": "ghi", "text": "d′ = −3d ⇒ 1/9 = 2/(3d) ⇒ d = 6 cm"}],
                tia_ao(6, h, f, 12, -22) + [{"loai": "vat", "x": -18, "h": 6, "ao": True, "ten": ["A′", "B′"], "mau": "max"},
                                            {"loai": "ghi", "text": "d = 6 cm < f = 9 cm: ảnh ảo, cùng chiều → kính lúp"}],
                [{"loai": "ghi", "text": "1/9 = 1/12 + 1/36 = 1/6 − 1/18 ✓"}],
            ]}


CONG_CU = [cc_d1, cc_d2, cc_d3, cc_d4]

# ═════════════ DẠNG (đề) ═════════════
DANG = [
    dict(label="Dạng 1 · Dễ · Kính lúp: đọc số bội giác, tìm tiêu cự, tính chất ảnh và so sánh hai kính", topic=TOPIC,
         problem_html=r"""<p>Vành một kính lúp ghi $2\times$. Lan đặt một bông hoa nhỏ cách kính $7{,}5\ \text{cm}$ rồi nhìn qua kính.</p><ol type="a"><li>Tính tiêu cự của kính.</li><li>Ảnh của bông hoa có tính chất nào?</li><li>Một kính lúp thứ hai ghi $5\times$. Tiêu cự của kính thứ hai ngắn hơn kính này bao nhiêu xentimét?</li></ol>"""),
    dict(label="Dạng 2 · Trung bình · Kính lúp: biết chỗ ảnh ảo hiện ra, tìm chỗ đặt vật và độ lớn ảnh", topic=TOPIC,
         problem_html=r"""<p>Kính lúp ghi $12{,}5\times$ được dùng để soi một con kiến cao $1{,}5\ \text{mm}$. Để mắt thấy ảnh ảo của con kiến hiện ra cách kính $6\ \text{cm}$ (cùng phía con kiến), hãy tính:</p><ol type="a"><li>tiêu cự của kính;</li><li>khoảng cách từ con kiến đến kính;</li><li>ảnh cao gấp mấy lần con kiến và cao bao nhiêu milimét.</li></ol>"""),
    dict(label="Dạng 3 · Trung bình · Nâng kính lúp lên: ảnh đổi thế nào và nâng thêm tối đa bao nhiêu", topic=TOPIC,
         problem_html=r"""<p>Kính lúp ghi $5\times$ đặt trên một đầu đinh ghim cao $2\ \text{mm}$, kính cách đầu đinh $3\ \text{cm}$. Giữ đinh đứng yên, Nam nâng kính lên thêm $1{,}5\ \text{cm}$.</p><ol type="a"><li>Tính tiêu cự của kính.</li><li>Trước khi nâng, ảnh của đầu đinh cao bao nhiêu milimét?</li><li>Sau khi nâng, ảnh cách kính bao nhiêu cm và cao bao nhiêu milimét?</li><li>Từ vị trí sau khi nâng, nâng kính thêm quá bao nhiêu cm nữa thì không còn thấy ảnh ảo, cùng chiều?</li></ol>"""),
    dict(label="Dạng 4 · Khó · Cho tỉ lệ ảnh và vật nhưng chưa nói ảnh thật hay ảo: tìm vị trí đặt vật", topic=TOPIC,
         problem_html=r"""<p>Một thấu kính hội tụ có tiêu cự $9\ \text{cm}$. Vật sáng $AB$ cao $2\ \text{cm}$, đặt vuông góc với trục chính, cho ảnh cao $6\ \text{cm}$.</p><ol type="a"><li>Tính khoảng cách từ vật đến thấu kính.</li><li>Với trường hợp ảnh hứng được trên màn, phải đặt màn cách thấu kính bao nhiêu cm để thấy ảnh rõ?</li><li>Trường hợp nào dùng thấu kính như một kính lúp?</li></ol>"""),
]

# ═════════════ BẢNG PHÂN TÍCH (cột 3: câu hỏi gợi, không ghi số đáp án) ═════════════
ANALYSIS = [
    [(r'''"Vành một kính lúp ghi $2\times$"''', r"$G=2$", r"Số ghi trên vành là đại lượng nào, liên hệ với $f$ ra sao?"),
     (r'''"đặt một bông hoa nhỏ cách kính $7{,}5\ \text{cm}$"''', r"$d=7{,}5\ \text{cm}$", r"⚠ Muốn biết ảnh thật hay ảo, $d$ được so với đại lượng nào của kính?"),
     (r'''"Ảnh của bông hoa có tính chất nào?"''', "thật hay ảo ; chiều ; lớn hay nhỏ", "Mỗi vùng của $d$ so với $f$ cho ảnh gì?"),
     (r'''"Một kính lúp thứ hai ghi $5\times$"''', r"$G_2=5$", "Từ số ghi trên vành tìm được đại lượng nào của kính thứ hai?"),
     (r'''"ngắn hơn kính này bao nhiêu xentimét"''', r"$f-f_2=\ ?$", "Hai tiêu cự được so sánh bằng phép tính nào?")],
    [(r'''"Kính lúp ghi $12{,}5\times$"''', r"$G=12{,}5$", "Từ $G$ tìm được đại lượng nào của kính?"),
     (r'''"con kiến cao $1{,}5\ \text{mm}$"''', r"$h=1{,}5\ \text{mm}$", "Chiều cao vật dùng ở bước nào?"),
     (r'''"ảnh ảo … cách kính $6\ \text{cm}$ (cùng phía con kiến)"''', r"$|d'|=6\ \text{cm}$", r"⚠ Ảnh ảo thì $d'$ mang dấu gì khi thế vào công thức thấu kính?"),
     (r'''"khoảng cách từ con kiến đến kính"''', r"$d=\ ?$", r"Công thức thấu kính nối $f$, $d$, $d'$ thế nào?"),
     (r'''"ảnh cao gấp mấy lần … cao bao nhiêu milimét"''', r"$k=\ ?$ ; $h'=\ ?$", r"Số phóng đại tính từ hai đại lượng nào? $h'$ liên hệ $h$ ra sao?")],
    [(r'''"Kính lúp ghi $5\times$"''', r"$G=5$", "Từ $G$ tìm được đại lượng nào của kính?"),
     (r'''"kính cách đầu đinh $3\ \text{cm}$"''', r"$d_1=3\ \text{cm}$", r"⚠ Kính lúp cho ảnh ảo, cùng chiều khi $d$ so với $f$ thế nào?"),
     (r'''"đầu đinh ghim cao $2\ \text{mm}$"''', r"$h=2\ \text{mm}$", "Chiều cao ảnh tính từ đại lượng nào?"),
     (r'''"Giữ đinh đứng yên, nâng kính lên thêm $1{,}5\ \text{cm}$"''', r"$d_2=\ ?$", "Khoảng cách từ đinh tới kính sau khi nâng là bao nhiêu?"),
     (r'''"ảnh cách kính bao nhiêu cm và cao bao nhiêu milimét"''', r"$d_2'=\ ?$ ; $h_2'=\ ?$", "Mỗi vị trí đều dùng chung công thức nào?"),
     (r'''"không còn thấy ảnh ảo, cùng chiều"''', r"$d_{\max}=\ ?$", "Mốc nào của $d$ làm ảnh đổi loại?")],
    [(r'''"thấu kính hội tụ có tiêu cự $9\ \text{cm}$"''', r"$f=9\ \text{cm}$", r"Dấu của $f$ với thấu kính hội tụ?"),
     (r'''"Vật sáng $AB$ cao $2\ \text{cm}$ … ảnh cao $6\ \text{cm}$"''', r"$h=2\ \text{cm}$ ; $h'=6\ \text{cm}$", "Hai chiều cao cho biết đại lượng nào?"),
     (r'''"cho ảnh cao $6\ \text{cm}$"''', "chưa nói ảnh thật hay ảo", r"⚠ Ảnh thật và ảnh ảo khác nhau ở dấu của đại lượng nào? Cần xét mấy trường hợp?"),
     (r'''"khoảng cách từ vật đến thấu kính"''', r"$d_1=\ ?$ ; $d_2=\ ?$", "Mỗi trường hợp, $d'$ liên hệ $d$ thế nào qua $k$?"),
     (r'''"đặt màn cách thấu kính"''', r"$d'=\ ?$", "Ảnh nào hứng được trên màn?"),
     (r'''"dùng thấu kính như một kính lúp"''', "vật ở vùng nào", "Kính lúp dùng vật ở vùng nào so với $f$?")],
]

# ═════════════ LỜI GIẢI + buoc[] (viết cùng lúc, số bước khớp 1-1) ═════════════
FOOT = "$f$ ngắn hơn thì $G$ lớn hơn ; ảnh ảo chỉ có khi vật nằm trong tiêu cự."
SOLS, STEPS = [], []

# ───── D1 ─────
SOLS.append(sol(
    [r"<strong>Kính lúp:</strong> thấu kính hội tụ tiêu cự ngắn ; vật trong tiêu cự ($d\lt f$) cho ảnh ảo, cùng chiều, lớn hơn.",
     r"<strong>Số bội giác:</strong> $G=\dfrac{25}{f}$ với $f$ tính bằng cm.",
     r"<strong>Công thức thấu kính:</strong> $\dfrac{1}{f}=\dfrac{1}{d}+\dfrac{1}{d'}$ ; $d'\lt0$ là ảnh ảo.",
     r"<strong>Điều kiện:</strong> so $d$ với $f$ trước khi kết luận ảnh thật hay ảo."],
    [("Tiêu cự", [P("Số ghi trên vành là $G$ :"), M(r"G=\dfrac{25}{f}\ \Rightarrow\ f=\dfrac{25}{G}=\dfrac{25}{2}"), A(r"f=12{,}5\ \text{cm}")]),
     ("Tính chất ảnh", [P("So $d$ với $f$ :"), M(r"d=7{,}5\ \text{cm}\ \lt\ f=12{,}5\ \text{cm}"),
                        A("T:Ảnh ảo, cùng chiều, lớn hơn bông hoa (nhìn qua kính, không hứng được trên màn).")]),
     ("Kính thứ hai", [P("Kính ghi $5\\times$ có tiêu cự :"), M(r"f_2=\dfrac{25}{G_2}=\dfrac{25}{5}=5\ \text{cm}"),
                       M(r"f-f_2=12{,}5-5"), A(r"f-f_2=7{,}5\ \text{cm}")]),
     ("Kiểm tra", [P(r"Thế lại : $\dfrac{1}{d'}=\dfrac{2}{25}-\dfrac{2}{15}=-\dfrac{4}{75}$, nên $d'=-18{,}75\ \text{cm}$ : $d'\lt0$ khớp ảnh ảo."),
                   P(r"$k=\dfrac{18{,}75}{7{,}5}=2{,}5$, khác $G=2$ vì $G$ ứng với ảnh ở rất xa."),
                   P("Kính thứ hai ghi số lớn hơn nên $f$ ngắn hơn ✓.")])],
    [r"a) $f=12{,}5\ \text{cm}$.", "b) Ảnh ảo, cùng chiều, lớn hơn bông hoa.", r"c) Ngắn hơn $7{,}5\ \text{cm}$ (kính $5\times$ có $f=5\ \text{cm}$)."],
    r"Nhận dạng : thấy <b>kính lúp ghi n×</b> → $f=25/G$, rồi so $d$ với $f$ để biết ảnh ảo hay thật."))

STEPS.append(dict(
    nhan_dang=r"Thấy <b>kính lúp ghi n×</b> → nghĩ tới <b>f = 25/G</b>, rồi so <b>d với f</b> để biết ảnh ảo hay thật",
    cap_do=1, fading="mo_het", go_roi={"buoc_hay_sai": 0},
    tom_de={"cho": [r"kính lúp ghi $2\times$", r"hoa cách kính $d=7{,}5\ \text{cm}$", r"kính thứ hai ghi $5\times$"],
            "tim": [r"a) $f$", "b) tính chất ảnh", r"c) $f_2$ ngắn hơn $f$ bao nhiêu cm"]},
    buoc=[
        buoc("Tiêu cự", "Tiêu cự của kính bằng bao nhiêu cm?", 12.5, "cm", 0.1,
             loi=r"Ra $0{,}08$ là chia ngược $f=\dfrac{G}{25}$ ; ra $50$ là nhân $25\cdot2$ ; ra $23$ là lấy $25-2$. Nhớ $G=\dfrac{25}{f}$."),
        buoc("Tính chất ảnh", "So $d$ với $f$: ảnh của bông hoa là ảnh nào?",
             loi=r"Áp “kính lúp thì ảnh ảo” mà không so $d$ với $f$ ; hoặc nhầm sang vùng cho ảnh thật, lớn hơn vật.",
             ke=[(r"So $d$ với $f$ để biết vật nằm vùng nào", True),
                 (r"Dùng $k=G$ để biết ảnh ảo hay thật", r"$k$ và $G$ cho độ lớn của ảnh, không cho biết ảnh thật hay ảo ; phải so $d$ với $f$."),
                 (r"Xem ảnh có to hơn vật không", r"Ảnh to hơn vật có ở cả ảnh thật ($f\lt d\lt2f$) lẫn ảnh ảo ; phải so $d$ với $f$ và $2f$.")],
             lua_chon=[("Ảnh ảo, cùng chiều, lớn hơn vật", True),
                       ("Ảnh thật, ngược chiều, lớn hơn vật", r"Ảnh thật chỉ có khi $d\gt f$ ; ở đây hoa nằm gần kính hơn tiêu điểm."),
                       ("Ảnh thật, ngược chiều, nhỏ hơn vật", r"Ảnh nhỏ hơn vật cần $d\gt2f$ ; ở đây vật gần kính hơn tiêu điểm.")]),
        buoc("Kính thứ hai", "Tiêu cự kính ghi $5\\times$ ngắn hơn kính này bao nhiêu cm?", 7.5, "cm", 0.1,
             loi=r"Ra $5$ là dừng ở $f_2$, chưa lấy hiệu ; ra $2{,}5$ là chia $12{,}5:5$ (tỉ số, không phải hiệu) ; ra $17{,}5$ là cộng thay vì trừ.",
             ke=[(r"Tính $f_2=\dfrac{25}{G_2}$ rồi lấy $f-f_2$", True),
                 (r"Số bội giác tăng $3$ nên tiêu cự giảm $3\ \text{cm}$", r"$G$ tỉ lệ nghịch với $f$, không tăng giảm đều ; phải tính $f_2$ từ $G_2=5$."),
                 (r"Chia $f:f_2$ để ra độ chênh", r"Phép chia cho tỉ số hai tiêu cự, không phải hiệu của chúng.")]),
        buoc("Kiểm tra"),
    ]))

# ───── D2 ─────
SOLS.append(sol(
    [r"<strong>Kính lúp:</strong> $G=\dfrac{25}{f}$, $f$ tính bằng cm.",
     r"<strong>Công thức thấu kính:</strong> $\dfrac{1}{f}=\dfrac{1}{d}+\dfrac{1}{d'}$ ; <strong>số phóng đại:</strong> $k=\dfrac{h'}{h}=\dfrac{|d'|}{d}$.",
     r"<strong>Điều kiện:</strong> ảnh ảo nằm cùng phía vật nên $d'\lt0$ : thế $d'=-6\ \text{cm}$, không phải $+6$.",
     r"$k$ khác $G$ : $G$ ứng với ảnh ở rất xa."],
    [("Tiêu cự", [M(r"G=\dfrac{25}{f}\ \Rightarrow\ f=\dfrac{25}{12{,}5}"), A(r"f=2\ \text{cm}")]),
     ("Vị trí đặt vật", [P("Ảnh ảo cùng phía vật nên $d'=-6\\ \\text{cm}$ :"),
                         M(r"\dfrac{1}{d}=\dfrac{1}{f}-\dfrac{1}{d'}=\dfrac{1}{2}+\dfrac{1}{6}=\dfrac{2}{3}"), A(r"d=1{,}5\ \text{cm}")]),
     ("Số phóng đại", [M(r"k=\dfrac{|d'|}{d}=\dfrac{6}{1{,}5}"), A(r"k=4\ \text{lần}"),
                       P("Khác $G=12{,}5$ : $G$ ứng với ảnh ở rất xa, còn ảnh ở $6\\ \\text{cm}$ thì $k$ tính từ $d$ và $d'$.")]),
     ("Chiều cao ảnh", [M(r"h'=k\,h=4\cdot1{,}5"), A(r"h'=6\ \text{mm}")]),
     ("Kiểm tra", [P(r"Thế lại : $\dfrac{1}{1{,}5}-\dfrac16=\dfrac12$ ✓."),
                   P(r"$d=1{,}5\ \text{cm}\lt f=2\ \text{cm}$ nên ảnh ảo, đúng như đề.")])],
    ["a) $f=2\\ \\text{cm}$.", "b) Con kiến cách kính $1{,}5\\ \\text{cm}$.", "c) Ảnh cao gấp $4$ lần, cao $6\\ \\text{mm}$."],
    r"Nhận dạng : thấy <b>ảnh ảo hiện cách kính … cm</b> → thế <b>d′ âm</b> vào công thức thấu kính để tìm $d$."))

STEPS.append(dict(
    nhan_dang=r"Thấy <b>ảnh ảo hiện cách kính … cm</b> → nghĩ tới <b>d′ âm</b>, thế vào công thức thấu kính để tìm <b>d</b>",
    cap_do=2, fading="giau_buoc_cuoi", go_roi={"buoc_hay_sai": 1},
    tom_de={"cho": [r"kính lúp $12{,}5\times$", r"kiến cao $1{,}5\ \text{mm}$", r"ảnh ảo cách kính $6\ \text{cm}$"],
            "tim": [r"a) $f$", "b) khoảng cách kiến–kính", "c) ảnh gấp mấy lần ; cao bao nhiêu mm"]},
    buoc=[
        buoc("Tiêu cự", "Tiêu cự của kính bằng bao nhiêu cm?", 2, "cm", 0.05,
             loi=r"Ra $0{,}5$ là chia ngược $f=\dfrac{G}{25}$ ; ra $312{,}5$ là nhân $25\cdot12{,}5$ ; ra $12{,}5$ là lấy luôn $G$."),
        buoc("Vị trí đặt vật", "Con kiến cách kính bao nhiêu cm?", 1.5, "cm", 0.05,
             loi=r"Thế $d'=+6\ \text{cm}$ ra $d=3\ \text{cm}$ : sai dấu vì ảnh ảo có $d'\lt0$. Lấy $d=6\ \text{cm}$ là nhầm vị trí vật với vị trí ảnh.",
             ke=[(r"Ảnh ảo nên thế $d'=-6\ \text{cm}$ vào $\dfrac{1}{f}=\dfrac{1}{d}+\dfrac{1}{d'}$", True),
                 (r"Thế $d'=+6\ \text{cm}$ vì ảnh cách kính $6\ \text{cm}$", r"Ảnh ảo nằm cùng phía vật nên $d'\lt0$ ; dấu dương chỉ dành cho ảnh thật."),
                 (r"Lấy luôn $d=6\ \text{cm}$ vì đề cho khoảng $6\ \text{cm}$", r"$6\ \text{cm}$ là khoảng từ ảnh tới kính, không phải từ vật tới kính.")]),
        buoc("Số phóng đại", "Ảnh cao gấp mấy lần con kiến?", 4, "lần", 0.05,
             loi=r"Ra $0{,}25$ là đảo thành $\dfrac{d}{|d'|}$ ; ra $12{,}5$ là lấy luôn $G$ ghi trên kính, nhưng $G$ ứng với ảnh ở rất xa chứ không phải ảnh cách kính $6\ \text{cm}$.",
             ke=[(r"$k=\dfrac{|d'|}{d}$", True),
                 (r"$k=G=12{,}5$", r"$G$ chỉ ứng với ảnh ở rất xa ; ở đây ảnh cách kính $6\ \text{cm}$ nên phải tính $\dfrac{|d'|}{d}$."),
                 (r"$k=\dfrac{d}{|d'|}$", r"Ảnh ảo qua kính lúp lớn hơn vật nên $k\gt1$ ; công thức bị đảo.")]),
        buoc("Chiều cao ảnh", "Ảnh cao bao nhiêu mm?", 6, "mm", 0.1,
             loi=r"Ra $18{,}75$ là nhân với $G=12{,}5$ ; ra $0{,}375$ là chia cho $k$ thay vì nhân.",
             ke=[(r"$h'=k\,h$", True),
                 (r"$h'=\dfrac{h}{k}$", r"Ảnh lớn hơn vật nên $h'\gt h$ : phải nhân với $k$."),
                 (r"$h'=|d'|\cdot h$", r"Số phóng đại là tỉ số $\dfrac{|d'|}{d}$, không phải $|d'|$ ; công thức này không có nghĩa vật lí.")]),
        buoc("Kiểm tra"),
    ]))

# ───── D3 ─────
SOLS.append(sol(
    [r"<strong>Kính lúp:</strong> $G=\dfrac{25}{f}$ ; vật trong tiêu cự ($d\lt f$) cho ảnh ảo, cùng chiều, lớn hơn.",
     r"<strong>Công thức thấu kính:</strong> $\dfrac{1}{f}=\dfrac{1}{d}+\dfrac{1}{d'}$ ; <strong>số phóng đại:</strong> $k=\dfrac{|d'|}{d}$.",
     r"<strong>Điều kiện:</strong> mỗi vị trí của kính là một giá trị $d$ khác, tính lại $d'$ và $k$ từ đầu.",
     r"Vượt $d=f$ thì ảnh ảo biến mất (ảnh ở rất xa, rồi lộn ngược)."],
    [("Tiêu cự", [M(r"f=\dfrac{25}{G}=\dfrac{25}{5}"), A(r"f=5\ \text{cm}")]),
     ("Ảnh trước khi nâng", [P(r"$d_1=3\ \text{cm}\lt f$ nên ảnh ảo, $d_1'\lt0$ :"),
                             M(r"\dfrac{1}{d_1'}=\dfrac{1}{f}-\dfrac{1}{d_1}=\dfrac{1}{5}-\dfrac{1}{3}=-\dfrac{2}{15}"),
                             M(r"k_1=\dfrac{|d_1'|}{d_1}=\dfrac{7{,}5}{3}=2{,}5"), A(r"h_1'=k_1\,h=2{,}5\cdot2=5\ \text{mm}")]),
     ("Ảnh sau khi nâng", [P(r"Kính cách đinh thêm $1{,}5\ \text{cm}$ : $d_2=3+1{,}5=4{,}5\ \text{cm}$, vẫn $\lt f$ nên vẫn ảnh ảo :"),
                           M(r"\dfrac{1}{d_2'}=\dfrac{1}{5}-\dfrac{1}{4{,}5}=-\dfrac{1}{45}"), A(r"|d_2'|=45\ \text{cm}")]),
     ("Chiều cao ảnh sau", [M(r"k_2=\dfrac{|d_2'|}{d_2}=\dfrac{45}{4{,}5}=10"), A(r"h_2'=k_2\,h=10\cdot2=20\ \text{mm}")]),
     ("Giới hạn nâng", [P(r"Ảnh còn ảo, cùng chiều khi $d\lt f$. Mốc là $d=f=5\ \text{cm}$ :"), M(r"f-d_2=5-4{,}5"),
                        A("T:Nâng thêm tối đa $0{,}5\\ \\text{cm}$ nữa ; quá mốc đó ảnh nhoè rồi lộn ngược.")]),
     ("Kiểm tra", [P(r"Thế lại : $\dfrac{1}{3}-\dfrac{2}{15}=\dfrac{1}{5}$ ✓ ; $\dfrac{1}{4{,}5}-\dfrac{1}{45}=\dfrac{1}{5}$ ✓."),
                   P(r"Nâng kính xa vật hơn thì ảnh ảo vừa xa hơn ($7{,}5\to45\ \text{cm}$) vừa to hơn ($k$ từ $2{,}5$ lên $10$) : đúng như khi soi con tem ở mở bài.")])],
    ["a) $f=5\\ \\text{cm}$.", "b) Ảnh cao $5\\ \\text{mm}$.", "c) Ảnh cách kính $45\\ \\text{cm}$, cao $20\\ \\text{mm}$.", "d) Nâng thêm tối đa $0{,}5\\ \\text{cm}$."],
    r"Nhận dạng : thấy <b>nâng kính / dịch vật</b> → mỗi vị trí là một $d$ mới, tính lại $d'$ và $k$ ; ảnh ảo chỉ còn khi $d\lt f$."))

STEPS.append(dict(
    nhan_dang=r"Thấy <b>nâng kính / dịch vật</b> → <b>d đổi</b>, tính lại <b>d′ và k</b> từng vị trí ; ảnh ảo cần $d\lt f$",
    cap_do=3, fading="giau_tu_buoc_2", go_roi={"buoc_hay_sai": 2},
    tom_de={"cho": [r"kính lúp $5\times$, cách đinh $3\ \text{cm}$", r"đầu đinh cao $2\ \text{mm}$", r"nâng kính thêm $1{,}5\ \text{cm}$"],
            "tim": [r"a) $f$", "b) ảnh cao (mm) trước khi nâng", "c) ảnh cách kính ; cao (mm) sau khi nâng", "d) nâng thêm tối đa (cm)"]},
    buoc=[
        buoc("Tiêu cự", "Tiêu cự của kính bằng bao nhiêu cm?", 5, "cm", 0.05,
             loi=r"Ra $0{,}2$ là chia ngược $f=\dfrac{G}{25}$ ; ra $125$ là nhân $25\cdot5$ ; ra $20$ là lấy $25-5$."),
        buoc("Ảnh trước khi nâng", "Trước khi nâng, ảnh cao bao nhiêu mm?", 5, "mm", 0.1,
             loi=r"Ra $10$ là lấy $k=G=5$ ; ra $3{,}3$ là lấy $k=\dfrac{f}{d}$. Số phóng đại phải tính từ $d'$ : $k=\dfrac{|d'|}{d}$.",
             ke=[(r"Thế $d=3\ \text{cm}$ và $f$ vào công thức thấu kính để tìm $d'$, rồi $k=\dfrac{|d'|}{d}$", True),
                 (r"Lấy $k=G$ rồi $h'=G\,h$", r"$G=\dfrac{25}{f}$ ứng với ảnh ở rất xa ; ảnh ở chỗ này có $k$ khác $G$."),
                 (r"Lấy $k=\dfrac{f}{d}$", r"Số phóng đại là $\dfrac{|d'|}{d}$ ; $\dfrac{f}{d}$ không phải $k$.")]),
        buoc("Ảnh sau khi nâng", "Sau khi nâng, ảnh cách kính bao nhiêu cm?", 45, "cm", 0.5,
             loi=r"Ra $7{,}5$ là dùng lại $d$ của lúc đầu ; ra $2{,}1$ là lấy $d=1{,}5\ \text{cm}$ (quãng nâng).",
             ke=[(r"Vật nay cách kính $d=3+1{,}5$ ; thế $d$ mới vào công thức thấu kính", True),
                 (r"Giữ nguyên $d=3\ \text{cm}$ vì đinh đứng yên", r"Đinh đứng yên nhưng kính dịch lên, nên khoảng cách từ đinh tới kính tăng thêm $1{,}5\ \text{cm}$."),
                 (r"Dùng $d=1{,}5\ \text{cm}$, là quãng nâng", r"$1{,}5\ \text{cm}$ chỉ là quãng dịch kính ; $d$ là khoảng từ đinh tới kính, gồm cả $3$ lúc đầu.")]),
        buoc("Chiều cao ảnh sau", "Sau khi nâng, ảnh cao bao nhiêu mm?", 20, "mm", 0.2,
             loi=r"Ra $5$ là dùng lại $k$ của lúc đầu ; ra $10$ là lấy $k=G$.",
             ke=[(r"$k=\dfrac{|d'|}{d}$ với $d'$ và $d$ mới", True),
                 (r"$k$ không đổi vì vẫn cùng một kính", r"$d$ đổi thì $d'$ đổi, nên $k$ đổi theo : đó là lý do ảnh to dần khi nâng kính."),
                 (r"$k=\dfrac{d}{|d'|}$", r"Ảnh ảo qua kính lúp lớn hơn vật nên $k\gt1$ ; công thức bị đảo.")]),
        buoc("Giới hạn nâng", "Từ lúc này, nâng kính thêm quá bao nhiêu cm nữa thì hết ảnh ảo, cùng chiều?", 0.5, "cm", 0.02,
             loi=r"Ra $2$ là tính từ vị trí lúc đầu (mốc trừ $d_1$ thay vì $d_2$) ; ra $5$ là lấy luôn tiêu cự.",
             ke=[(r"Ảnh còn ảo, cùng chiều khi $d\lt f$ ; tìm $f-d$ tại vị trí hiện tại", True),
                 (r"Ảnh còn ảo, cùng chiều khi $d\lt2f$ ; tìm $2f-d$", r"Vùng $f\lt d\lt2f$ cho ảnh thật, ngược chiều ; mốc đổi loại ảnh là $f$."),
                 ("Nâng bao nhiêu cũng còn ảnh ảo vì là kính lúp", r"Kính lúp chỉ cho ảnh ảo khi vật trong tiêu cự ; vượt tiêu điểm thì ảnh lộn ngược.")]),
        buoc("Kiểm tra"),
    ]))

# ───── D4 ─────
SOLS.append(sol(
    [r"<strong>Công thức thấu kính:</strong> $\dfrac{1}{f}=\dfrac{1}{d}+\dfrac{1}{d'}$ ; <strong>số phóng đại:</strong> $k=\dfrac{h'}{h}=\dfrac{|d'|}{d}$.",
     r"<strong>Ảnh thật:</strong> $d'\gt0$, ngược chiều, hứng được trên màn. <strong>Ảnh ảo:</strong> $d'\lt0$, cùng chiều, không hứng được.",
     r"<strong>Điều kiện:</strong> đề chỉ cho $k$ nên $|d'|=k\,d$ ứng với <strong>cả hai</strong> dấu của $d'$ : xét hai trường hợp.",
     r"<strong>Kính lúp:</strong> vật trong tiêu cự ($d\lt f$), ảnh ảo."],
    [("Số phóng đại", [M(r"k=\dfrac{h'}{h}=\dfrac{6}{2}"), A(r"k=3")]),
     ("Ảnh thật : vị trí vật", [P(r"Ảnh thật nên $d'\gt0$ và $|d'|=k\,d$, suy ra $d'=3d$ :"),
                                M(r"\dfrac{1}{f}=\dfrac{1}{d}+\dfrac{1}{3d}=\dfrac{4}{3d}"), M(r"d=\dfrac{4f}{3}=\dfrac{4\cdot9}{3}"), A(r"d_1=12\ \text{cm}")]),
     ("Vị trí màn", [M(r"d_1'=3\,d_1=3\cdot12"), A(r"d_1'=36\ \text{cm}"), P("Màn đặt cách thấu kính $36\\ \\text{cm}$ thì hứng được ảnh thật rõ nét.")]),
     ("Ảnh ảo : vị trí vật", [P(r"Ảnh ảo nên $d'\lt0$ và $|d'|=k\,d$, suy ra $d'=-3d$ :"),
                              M(r"\dfrac{1}{f}=\dfrac{1}{d}-\dfrac{1}{3d}=\dfrac{2}{3d}"), M(r"d=\dfrac{2f}{3}=\dfrac{2\cdot9}{3}"), A(r"d_2=6\ \text{cm}")]),
     ("Dùng làm kính lúp", [P("Kính lúp cần ảnh ảo, cùng chiều, nên vật phải ở trong tiêu cự :"), M(r"d_2=6\ \text{cm}\ \lt\ f=9\ \text{cm}"),
                            A("T:Dùng vị trí $d_2=6\\ \\text{cm}$ (ảnh ảo) làm kính lúp ; vị trí $d_1=12\\ \\text{cm}$ cho ảnh thật, ngược chiều, hứng được trên màn.")]),
     ("Kiểm tra", [P(r"Thế lại : $\dfrac{1}{12}+\dfrac{1}{36}=\dfrac19$ ✓ ; $\dfrac16-\dfrac1{18}=\dfrac19$ ✓."),
                   P(r"Cùng $k=3$ mà hai kiểu ảnh : $d=\dfrac43f$ cho ảnh thật, $d=\dfrac23f$ cho ảnh ảo.")])],
    ["a) $d_1=12\\ \\text{cm}$ (ảnh thật) và $d_2=6\\ \\text{cm}$ (ảnh ảo).", "b) Màn cách thấu kính $36\\ \\text{cm}$.", "c) Vị trí $d_2=6\\ \\text{cm}$ (ảnh ảo)."],
    r"Nhận dạng : thấy <b>ảnh gấp k lần</b> mà chưa nói thật hay ảo → xét <b>hai trường hợp</b> $d'=+kd$ và $d'=-kd$."))

STEPS.append(dict(
    nhan_dang=r"Thấy <b>ảnh gấp k lần</b> mà chưa nói thật hay ảo → xét <b>hai trường hợp</b> <b>d′ = +kd</b> và <b>d′ = −kd</b>",
    cap_do=4, fading="giau_het", go_roi={"buoc_hay_sai": 3},
    tom_de={"cho": [r"thấu kính hội tụ $f=9\ \text{cm}$", r"vật cao $2\ \text{cm}$, ảnh cao $6\ \text{cm}$"],
            "tim": ["a) khoảng cách vật–kính", "b) màn cách kính (ảnh thật)", "c) vị trí dùng làm kính lúp"]},
    buoc=[
        buoc("Số phóng đại", "Ảnh cao gấp mấy lần vật?", 3, "lần", 0.05,
             loi=r"Ra $\dfrac13$ là đảo thành $\dfrac{h}{h'}$ ; ra $4$ là lấy hiệu $6-2$ thay vì tỉ số."),
        buoc("Ảnh thật : vị trí vật", "Nếu ảnh là ảnh thật thì vật cách thấu kính bao nhiêu cm?", 12, "cm", 0.1,
             loi=r"Thế $d'=-3d$ ra vị trí khác (ảnh ảo), không phải ảnh thật ; ra $27$ là lấy $d=k\,f$.",
             ke=[(r"Ảnh thật : $d'=3d$ ; thế vào $\dfrac{1}{f}=\dfrac{1}{d}+\dfrac{1}{d'}$", True),
                 (r"Ảnh thật : $d'=-3d$", r"Dấu âm của $d'$ là ảnh ảo ; ảnh thật có $d'\gt0$ và $|d'|=k\,d$."),
                 (r"Ảnh thật : $d'=\dfrac{d}{3}$", r"$k=\dfrac{|d'|}{d}=3$ nên $|d'|=3d$, không phải $\dfrac d3$.")]),
        buoc("Vị trí màn", "Màn đặt cách thấu kính bao nhiêu cm?", 36, "cm", 0.5,
             loi=r"Ra $12$ là lấy luôn khoảng cách vật ; ra $9$ là lấy tiêu cự ; ra $4$ là lấy $\dfrac{d}{3}$.",
             ke=[(r"Màn đặt tại chỗ có ảnh thật : $d'=3d$ với $d$ vừa tìm", True),
                 (r"Màn đặt tại tiêu điểm $F'$", r"Ảnh thật hiện ở $d'$ tính được ; chỉ vật ở rất xa mới cho ảnh tại $F'$."),
                 (r"Màn đặt cách kính đúng bằng khoảng cách vật", r"$d'=d$ chỉ khi $d=2f$ ; ở đây ảnh lớn hơn vật nên $d'\gt d$.")]),
        buoc("Ảnh ảo : vị trí vật", "Nếu ảnh là ảnh ảo thì vật cách thấu kính bao nhiêu cm?", 6, "cm", 0.1,
             loi=r"Thế $d'=+3d$ lại ra đúng vị trí của ảnh thật ; ra $27$ là lấy $d=k\,f$.",
             ke=[(r"Ảnh ảo : $d'=-3d$ ; thế vào công thức thấu kính", True),
                 (r"Ảnh ảo : $d'=+3d$, giống trường hợp trước", r"Ảnh ảo có $d'\lt0$ ; dùng $d'=+3d$ sẽ ra lại vị trí của ảnh thật."),
                 (r"Ảnh ảo : $d=3f$ vì $k=3$", r"Không có công thức $d=k\,f$ ; phải dùng $|d'|=k\,d$ rồi thế vào công thức thấu kính.")]),
        buoc("Dùng làm kính lúp", "Dùng thấu kính như kính lúp thì đặt vật ở vị trí nào?",
             loi=r"Chọn vị trí cho ảnh thật vì thấy ảnh “lớn hơn vật” ; ảnh thật lộn ngược, không phải cách dùng kính lúp.",
             lua_chon=[("Vị trí cho ảnh ảo, vật trong tiêu cự", True),
                       ("Vị trí cho ảnh thật, vì ảnh lớn hơn vật", r"Ảnh thật hứng được trên màn nhưng ngược chiều ; kính lúp dùng ảnh ảo, cùng chiều, nhìn qua kính."),
                       ("Cả hai vị trí đều dùng được", r"Chỉ vật trong tiêu cự ($d\lt f$) mới cho ảnh ảo, cùng chiều để nhìn qua kính.")],
             ke=[(r"So $d$ của hai vị trí với $f$", True),
                 (r"Chọn vị trí có $|d'|$ lớn hơn", r"Độ lớn của $d'$ không quyết định có phải kính lúp hay không ; phải xem $d$ so với $f$."),
                 (r"Chọn vị trí có ảnh lớn hơn", r"Hai vị trí cho ảnh cao bằng nhau ($6\ \text{cm}$).")]),
        buoc("Kiểm tra"),
    ]))

assert len(DANG) == len(ANALYSIS) == len(SOLS) == len(STEPS) == len(CONG_CU) == 4
for s, c in zip(STEPS, CONG_CU):
    assert len(c()["lop"]) == len(s["buoc"]), (len(c()["lop"]), len(s["buoc"]))


# ═════════════ Ghi file ═════════════
BUILD = [lambda k: ""] * len(DANG)          # "một dạng — một hình": không còn <figure> mô phỏng / hình dữ kiện
write(J, 88, "Bài 10. Kính lúp. Bài tập thấu kính", DANG, BUILD, ANALYSIS, SOLS)
inject(J, BUILD, ANALYSIS, SOLS, STEPS)
d = json.load(open(J))
d["generated_at"] = "2026-11-10"
d["review"] = {"checked": False, "notes": "chờ kiểm chéo (kiem-code) + soát ảnh /dev/btm"}
FORM = ["ly_thuyet", "ly_thuyet", "ly_thuyet", "bai_tap"]
for i, q in enumerate(d["dang_bai"]):
    q["form"] = FORM[i]
    q["cong_cu"] = CONG_CU[i]()
    q["cong_cu"]["de"] = True
json.dump(d, open(J, "w"), ensure_ascii=False, indent=1)
txt = open(J, encoding="utf8").read()
bad = re.findall(r"[\x00-\x08\x0b\x0c\x0e-\x1f]", json.dumps(json.load(open(J)), ensure_ascii=False))
assert not bad, "ký tự điều khiển trong JSON"
assert "marker-end" not in txt and "<figure" not in txt
print("ghi", J, len(d["dang_bai"]), "dạng")
