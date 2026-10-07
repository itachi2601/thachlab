"""Bài 10. Kính lúp. Bài tập thấu kính (KHTN 9, lesson_id 88).
Sinh 4 hình SVG + bảng số liệu thí nghiệm + 3 file content/thi-nghiem/tn-l9-kinhlup-0N.json,
thay mốc <!--FIGn--> / __...__ trong theory.src.html -> theory.html.
Mọi ảnh tính bằng 1/f = 1/d + 1/d' (d' < 0: ảnh ảo); toạ độ tia kiểm bằng assert.
Chạy: cd <thư mục bài> && python3 build_figs.py
"""
import json, math, pathlib
from svg_lib import *

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[2]
PHUT = 17          # số phút đọc: lấy từ lint_do_dai.py, làm tròn lên


def vn(x, nd=1):
    """Số thập phân kiểu Việt trong $…$."""
    s = f"{x:.{nd}f}"
    if "." in s:
        s = s.rstrip("0").rstrip(".")
    return s.replace(".", "{,}")


def img(d, f):
    """d' theo 1/f = 1/d + 1/d' (d' âm: ảnh ảo) và k = |d'|/d."""
    dp = d * f / (d - f)
    return dp, abs(dp) / d


def line(x1, y1, x2, y2, c="currentColor", w=2, dash="", op=1):
    da = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{c}" stroke-width="{w}"{da} opacity="{op}"/>'


def ray(x1, y1, x2, y2, c=RED, w=2.4, at=0.55):
    """Tia sáng: nét liền + đầu V 30° giữa tia, chỉ chiều truyền."""
    mx, my = x1 + (x2 - x1) * at, y1 + (y2 - y1) * at
    L = math.hypot(x2 - x1, y2 - y1)
    if L < 30:                                     # đoạn quá ngắn: bỏ đầu V cho khỏi rối
        return line(x1, y1, x2, y2, c, w)
    return line(x1, y1, x2, y2, c, w) + chevron(mx, my, x2 - x1, y2 - y1, c, 2.2, 9 if L < 60 else 12)


def ext(x1, y1, x2, y2):
    """Đường kéo dài ngược (không có ánh sáng): nét đứt xanh."""
    return line(x1, y1, x2, y2, BLUE, 1.8, "6 5", .95)


def vec(x, y0, y1, c, w=3, dash=""):
    """Mũi tên vật/ảnh vuông góc trục chính, chân ở (x, y0), đầu ở (x, y1)."""
    return line(x, y0, x, y1, c, w, dash) + chevron(x, y1, 0, y1 - y0, c, 2.4, 11)


def lens(x, y0, H):
    """Ký hiệu thấu kính hội tụ: đoạn thẳng, hai đầu V hướng ra ngoài."""
    g = f'<ellipse cx="{x}" cy="{y0}" rx="9" ry="{H}" fill="rgba(56,189,248,.14)" stroke="none"/>'
    return g + line(x, y0 - H, x, y0 + H, "currentColor", 2.4) + chevron(x, y0 - H, 0, -1, "currentColor", 2.4, 11) + chevron(x, y0 + H, 0, 1, "currentColor", 2.4, 11)


def axis(x1, x2, y0):
    return line(x1, y0, x2, y0, "currentColor", 1.4, "", .7)


def dot(x, y, c="currentColor", r=3.5):
    return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{c}"/>'


def on_line(p, q, r, tol=0.6):
    """r nằm trên đường thẳng pq (khoảng cách < tol px)."""
    (x1, y1), (x2, y2), (x3, y3) = p, q, r
    return abs((x2 - x1) * (y3 - y1) - (y2 - y1) * (x3 - x1)) / math.hypot(x2 - x1, y2 - y1) < tol


def prime(s):
    return s.replace("'", "’")


def lens_scene(Ox, y0, s, f, d, hpx, H=None, labels=True, lab_size=17, xmax=412):
    """Dựng ảnh qua thấu kính hội tụ bằng hai tia đặc biệt. Trả (svg, thông tin).
    s: px/cm theo trục chính; hpx: chiều cao vật (px, trục đứng có tỉ lệ riêng — phép co giãn affine giữ nguyên giao điểm)."""
    dp, k = img(d, f)
    Ax, Bx, By = Ox - d * s, Ox - d * s, y0 - hpx
    Fx, Fpx = Ox - f * s, Ox + f * s
    real = dp > 0
    Apx = Ox + dp * s                       # ảnh thật bên phải, ảnh ảo bên trái (dp < 0)
    Bpy = y0 + k * hpx if real else y0 - k * hpx
    I1 = (Ox, By)                           # điểm tới của tia song song
    # kiểm: B' nằm trên đường (I1, F') và đường (B, O)
    assert on_line(I1, (Fpx, y0), (Apx, Bpy)), "tia 1 không qua B'"
    assert on_line((Bx, By), (Ox, y0), (Apx, Bpy)), "tia 2 không qua B'"
    H = H or max(hpx, k * hpx if not real else hpx) + 22
    g = axis(10, xmax, y0) + lens(Ox, y0, H)
    g += dot(Fx, y0) + dot(Fpx, y0) if Fpx <= xmax else dot(Fx, y0)
    # tia 1: B -> I1 -> qua F' (kéo dài tới mép hoặc tới B' nếu ảnh thật)
    g += ray(Bx, By, Ox, By, at=0.55 if real else 0.75)
    if real:
        g += ray(Ox, By, Apx, Bpy, at=0.5)
    else:
        t = min((xmax - 8 - Ox) / (Fpx - Ox), 1.25)
        g += ray(Ox, By, Ox + (Fpx - Ox) * t, By + (y0 - By) * t, at=0.6)
        g += ext(Ox, By, Apx, Bpy)
    # tia 2: B -> O -> đi thẳng
    if real:
        g += ray(Bx, By, Ox, y0) + ray(Ox, y0, Apx, Bpy, at=0.5)
    else:
        t2 = min((xmax - 40 - Ox) / (Ox - Bx), 80 / hpx)
        g += ray(Bx, By, Ox, y0, at=0.3) + ray(Ox, y0, Ox + (Ox - Bx) * t2, y0 + (y0 - By) * t2, at=0.6)
        g += ext(Bx, By, Apx, Bpy)
    g += vec(Ax, y0, By, ORG)
    g += vec(Apx, y0, Bpy, BLUE, 3, "" if real else "6 4")
    info = dict(dp=dp, k=k, Ax=Ax, By=By, Apx=Apx, Bpy=Bpy, Fx=Fx, Fpx=Fpx, real=real, H=H)
    return g, info


# ---------- Hình 1: cảnh soi con tem (nhìn ngang). Không vẽ tia, không vẽ ảnh → không lộ đáp án dự đoán.
b = line(20, 262, 400, 262, "currentColor", 2.4)
b += '<rect x="168" y="250" width="84" height="10" rx="1" fill="rgba(251,146,60,.35)" stroke="#fb923c" stroke-width="2" stroke-dasharray="3 2"/>'
b += '<ellipse cx="210" cy="168" rx="62" ry="9" fill="rgba(56,189,248,.18)" stroke="currentColor" stroke-width="2.4"/>'
b += line(272, 168, 352, 148, "currentColor", 7) + line(272, 168, 352, 148, ORG, 3)
b += '<path d="M178,62 Q210,38 242,62 Q210,82 178,62 Z" fill="none" stroke="currentColor" stroke-width="2.2"/>' + dot(210, 62, "currentColor", 6)
b += line(210, 84, 210, 156, "currentColor", 1.5, "4 5", .6) + line(210, 180, 210, 248, "currentColor", 1.5, "4 5", .6)
b += line(110, 226, 110, 140, GRN, 2.6) + chevron(110, 140, 0, -1, GRN, 2.6, 12)
b += text(122, 206, "nâng", GRN, 17, "start", "700") + text(122, 226, "dần lên", GRN, 17, "start", "700")
b += text(262, 256, "con tem", ORG, 17, "start", "700")
b += text(300, 132, "kính lúp", "currentColor", 17, "start", "700")
b += text(252, 58, "mắt", "currentColor", 17, "start", "700")
fig1 = wrap("0 0 420 280", "Nhìn ngang: con tem nằm trên bàn, kính lúp cầm phía trên, mắt nhìn từ trên xuống qua kính, kính được nâng dần lên", b,
            "Hình 1. Mắt nhìn qua kính lúp xuống con tem, rồi nâng kính dần lên.")

# ---------- Hình 2: dựng ảnh qua kính lúp (f = 10 cm, d = 5 cm → d' = -10 cm, k = 2)
F2, D2 = 10, 5
g2, i2 = lens_scene(Ox=270, y0=200, s=12, f=F2, d=D2, hpx=46, H=96, xmax=412)
assert i2["dp"] < 0 and abs(i2["Apx"] - i2["Fx"]) < 0.5 and abs(i2["k"] - 2) < 1e-9   # ảnh ảo đúng tại F, cao gấp đôi
b = g2
y0 = 200
b += text(i2["Fx"] - 4, y0 + 26, "F", "currentColor", 17, "end", "700") + text(i2["Fpx"], y0 + 26, "F'", "currentColor", 17, "middle", "700")
b += text(270 + 8, y0 + 26, "O", "currentColor", 17, "start", "700")
b += text(i2["Ax"] + 6, y0 + 22, "A", ORG, 17, "start", "700") + text(i2["Ax"] - 8, i2["By"] + 4, "B", ORG, 17, "end", "700")
b += text(i2["Apx"] - 8, i2["Bpy"] + 4, "B'", BLUE, 17, "end", "700")
b += text(i2["Apx"] - 30, y0 - 16, "A'", BLUE, 17, "end", "700")
b += text(16, 34, "ảnh ảo A'B'", BLUE, 17, "start", "700")
b += text(16, 56, "(nét đứt)", BLUE, 17, "start", "600")
b += text(300, 34, "mắt ở phía", "currentColor", 17, "start", "600") + text(300, 56, "này →", "currentColor", 17, "start", "600")
fig2 = wrap("0 0 420 320", "Vật AB nằm trong khoảng tiêu cự của kính lúp; tia song song trục chính ló qua F', tia qua O đi thẳng; kéo dài ngược hai tia ló gặp nhau tại B', ảnh ảo A'B' cùng chiều, lớn hơn vật", b,
            "Hình 2. Vật AB trong khoảng tiêu cự. Hai tia ló loe ra; đường kéo dài ngược (nét đứt xanh) gặp nhau ở B'. Ảnh A'B' là ảnh ảo, cùng chiều, lớn hơn vật.")

# ---------- Hình 3: ba trường hợp của bài mẫu 1 (f = 10 cm; d = 30, 15, 6 cm). Hình nằm trong <details> (~290 px) → chữ 20.
F3, H_NEN = 10, 6
FS3 = 20
CASES = ((30, 84, "(a) d = 30 cm"), (15, 232, "(b) d = 15 cm"), (6, 466, "(c) d = 6 cm"))
b, info3 = "", []
for d, y0, cap in CASES:
    g, inf = lens_scene(Ox=200, y0=y0, s=6, f=F3, d=d, hpx=36, H=48 if d != 6 else 92, xmax=412)
    b += g
    b += text(inf["Fx"], y0 + 26, "F", "currentColor", FS3, "middle", "700")
    b += text(inf["Fpx"] + 6, y0 - 8, "F'", "currentColor", FS3, "start", "700")      # trên trục, bên phải F': không tia nào đi qua
    b += text(200 - 8, y0 + 26, "O", "currentColor", FS3, "end", "700")
    if d != 6:                                       # chấm 2F phía vật: lời giải so d với 2f
        x2f = 200 - 2 * F3 * 6
        b += dot(x2f, y0) + text(x2f, y0 + 26, "2F", "currentColor", FS3, "middle", "700")
    if inf["real"]:
        b += text(inf["Apx"] + 10, inf["Bpy"] + 8, "B'", BLUE, FS3, "start", "700")
    else:
        b += text(inf["Apx"] - 10, inf["Bpy"] - 6, "B'", BLUE, FS3, "end", "700")
    b += (text(inf["Ax"] - 8, inf["By"] + 22, "B", ORG, FS3, "end", "700") if d == 6 else text(inf["Ax"] - 4, inf["By"] - 8, "B", ORG, FS3, "middle", "700"))
    b += text(410, y0 - 52 if d != 6 else y0 - 92, cap, GRN, FS3, "end", "700")
    info3.append((d, inf))
b += line(10, 158, 410, 158, "currentColor", 1, "", .3) + line(10, 340, 410, 340, "currentColor", 1, "", .3)
fig3 = wrap("0 0 420 580", "Ba trường hợp vật đặt trước thấu kính hội tụ f = 10 cm: d = 30 cm cho ảnh thật nhỏ hơn, d = 15 cm cho ảnh thật lớn hơn, d = 6 cm cho ảnh ảo cùng chiều lớn hơn", b,
            "Hình 3. Ngọn nến (cam) và ảnh (xanh) qua thấu kính f = 10 cm. Ảnh thật vẽ nét liền ở bên kia thấu kính; ảnh ảo vẽ nét đứt, cùng phía vật.")
fig3 = fig3.replace('<figure class="fig" data-tl="1">', '<figure class="fig" data-tl="1" data-exp="tn-l9-kinhlup-03">', 1)

TINH_CHAT = {30: "thật, ngược chiều, nhỏ hơn vật", 15: "thật, ngược chiều, lớn hơn vật", 6: "ảo, cùng chiều, lớn hơn vật"}
VUNG = {30: "d \\gt 2f", 15: "f \\lt d \\lt 2f", 6: "d \\lt f"}
li = []
for (d, inf), tag in zip(info3, "abc"):
    li.append(f"<li>({tag}) $d = {d}\\ \\text{{cm}}$, ${VUNG[d]}$: ảnh {TINH_CHAT[d]}; tính ra $d' = {vn(inf['dp'])}\\ \\text{{cm}}$, "
              f"ảnh cao ${vn(H_NEN * inf['k'])}\\ \\text{{cm}}.$</li>")
BA_TH = "\n".join(li)
assert [round(i["dp"], 6) for _, i in info3] == [15, 30, -15]

# ---------- Hình 4: bài mẫu 3 (kính lúp 2,5x → f = 10 cm; chữ in d = 8 cm → d' = -40 cm, k = 5). Đặt ngoài <details>, sau Câu 7.
F4, D4 = 25 / 2.5, 8
FS4 = 18
g4, i4 = lens_scene(Ox=335, y0=150, s=7, f=F4, d=D4, hpx=18, H=56, xmax=412)
assert abs(i4["dp"] + 40) < 1e-9 and abs(i4["k"] - 5) < 1e-9 and abs(i4["Apx"] - 55) < 1e-6
b = g4
y0 = 150
b += text(i4["Fx"] - 4, y0 + 26, "F", "currentColor", FS4, "end", "700") + text(i4["Fpx"] - 2, y0 + 26, "F'", "currentColor", FS4, "end", "700")
b += text(i4["Ax"] + 4, y0 + 26, "A", ORG, FS4, "start", "700")
b += text(335 + 8, y0 + 26, "O", "currentColor", FS4, "start", "700")
b += text(i4["Apx"] - 10, i4["Bpy"] + 4, "B'", BLUE, FS4, "end", "700")
b += text(i4["Apx"] + 4, y0 + 26, "A'", BLUE, FS4, "middle", "700")
b += line(i4["Apx"], y0 + 48, 335, y0 + 48, "currentColor", 1.2, "", .7)
b += text((i4["Apx"] + 335) / 2, y0 + 70, "40 cm", "currentColor", FS4, "middle", "700")
fig4 = wrap("0 0 420 232", "Chữ in AB cách kính lúp 8 cm, trong khoảng tiêu cự 10 cm; ảnh ảo A'B' cùng chiều, cao gấp 5 lần, cách kính 40 cm về phía chữ", b,
            "Hình 4. Bài mẫu 3: chữ in AB cách kính 8 cm, ảnh ảo A'B' cách kính 40 cm, cao gấp 5 lần.")

# ---------- Bảng số liệu thí nghiệm 1 (minh hoạ): kính f = 5 cm, đèn cách 300 cm
F1, DEN = 5.0, 300.0
dp_mh = DEN * F1 / (DEN - F1)                       # ≈ 5,08 cm: vị trí ảnh thật, hơi xa hơn F
LECH = (0.1, -0.1, 0.2, 0.0, -0.1)                  # sai số đặt giấy (ảnh rõ nhất khó xác định), cm
DO = [round(dp_mh + e, 1) for e in LECH]
mean = sum(DO) / len(DO)
G_do = 25 / mean
devs = [abs(x - mean) for x in DO]
mx = max(devs)
worst = [n for n, dv in enumerate(devs, 1) if abs(dv - mx) < 1e-6]
assert len(worst) == 1 and abs(dp_mh - 5.08) < 0.01
bang = "\n".join(f"<tr><td>Lần {n}</td><td>${vn(x)}\\ \\text{{cm}}$</td></tr>" for n, x in enumerate(DO, 1))
nx = (f"trung bình ${vn(mean, 2)}\\ \\text{{cm}}$, nên $G = 25/{vn(mean, 2)} \\approx {vn(G_do, 1)}$, khớp số 5x trên vành. "
      f"Lần {worst[0]} lệch nhiều nhất (${vn(DO[worst[0] - 1])}\\ \\text{{cm}}$) vì chỗ ảnh rõ nhất khó xác định. "
      f"Số đo hơi lớn hơn $5\\ \\text{{cm}}$ còn vì đèn chưa ở xa vô cùng: theo công thức thấu kính, ảnh của đèn cách kính khoảng ${vn(dp_mh, 2)}\\ \\text{{cm}}.$ "
      f"Đặt đèn càng xa, đo nhiều lần lấy trung bình thì càng chính xác.")

h = (HERE / "theory.src.html").read_text(encoding="utf8")
h = (h.replace("__BANG_TN1__", bang).replace("__NHAN_XET_TN1__", nx).replace("__BA_TRUONG_HOP__", BA_TH)
      .replace("__PHUT__", str(PHUT)))
for n, f in enumerate((fig1, fig2, fig3, fig4), 1):
    assert h.count(f"<!--FIG{n}-->") == 1, n
    h = h.replace(f"<!--FIG{n}-->", f)
assert "__" not in h.replace("___", "")


def punct_in_math(t):
    """Dấu câu liền sau công thức nội dòng đưa vào trong $…$ (khỏi rơi xuống dòng riêng)."""
    out, parts = [], t.split("$$")
    for n, part in enumerate(parts):
        if n % 2:                                   # bên trong $$…$$
            out.append(part); continue
        seg, i = [], 0
        while True:
            a = part.find("$", i)
            if a < 0:
                seg.append(part[i:]); break
            b = part.find("$", a + 1)
            assert b > 0, part[a:a + 60]
            seg.append(part[i:a]); body = part[a + 1:b]; j = b + 1
            while j < len(part) and part[j] in ",.;:" and not body.rstrip().endswith(tuple(",.;:")):
                body += "{:}" if part[j] == ":" else part[j]; j += 1
            seg.append("$" + body + "$"); i = j
        out.append("".join(seg))
    return "$$".join(out)


h = punct_in_math(h)
(HERE / "theory.html").write_text(h, encoding="utf8")

# ---------- Kho thí nghiệm
BAI = "Bài 10. Kính lúp. Bài tập thấu kính"
SRC = "content/lesson-samples/l9-kinh-lup-bai-tap-thau-kinh/theory.html"
base = {"mon": "vat-ly", "lop": 9, "bai": BAI, "lesson_id": 88, "nguon_trong_bai": SRC}
tn = []
tn.append({**base,
  "id": "tn-l9-kinhlup-01", "ten": "Đo tiêu cự kính lúp ghi 5x bằng ảnh của bóng đèn ở xa", "loai": "thi_nghiem", "muc_do": "trung_binh",
  "kien_thuc": ["kinhlup.cau_tao", "kinhlup.so_boi_giac", "thaukinh.tieu_cu"],
  "muc_tieu": "Đo gần đúng tiêu cự kính lúp rồi kiểm số bội giác G = 25/f với số ghi trên vành kính.",
  "dung_cu": [{"ten": "Kính lúp ghi 5x", "so_luong": 1}, {"ten": "Bóng đèn sáng đặt cách khoảng 3 m", "so_luong": 1},
              {"ten": "Tờ giấy trắng làm màn", "so_luong": 1}, {"ten": "Thước có vạch chia mm", "so_luong": 1}],
  "cac_buoc": {"lam": ["Bật bóng đèn ở cuối lớp, cách kính khoảng 3 m.",
                       "Đặt tờ giấy sau kính, dịch tới khi ảnh bóng đèn nhỏ và rõ nhất.",
                       "Đo khoảng cách từ kính tới giấy; làm 5 lần."],
               "quan_sat": ["Ảnh bóng đèn rõ nét, ngược chiều, hứng được trên giấy.", "Khoảng cách đo được gần 5 cm."],
               "rut_ra": ["Vật ở rất xa thì ảnh hiện gần tiêu điểm: khoảng cách đo xấp xỉ f.",
                          "G = 25/f tính từ f đo được khớp số 5x trên vành kính."]},
  "tham_so": [{"ky_hieu": "f", "ten": "Tiêu cự kính lúp", "don_vi": "cm", "kieu": "co_dinh", "gia_tri": F1},
              {"ky_hieu": "D", "ten": "Khoảng cách đèn → kính", "don_vi": "cm", "kieu": "dieu_chinh", "min": 50, "max": 600, "mac_dinh": DEN, "buoc": 50},
              {"ky_hieu": "d'", "ten": "Khoảng cách kính → giấy khi ảnh rõ nhất", "don_vi": "cm", "kieu": "do_duoc", "sai_so_do": 0.2},
              {"ky_hieu": "G", "ten": "Số bội giác", "don_vi": "", "kieu": "tinh_ra"}],
  "mo_hinh": {"phuong_trinh": ["1/f = 1/D + 1/d'", "d' = D·f/(D − f)", "G = 25/f (f tính bằng cm)"],
              "gia_thiet": ["thấu kính mỏng", "đèn coi như vật điểm trên trục chính", "sai số chủ yếu do chọn chỗ ảnh rõ nhất (±0,2 cm)"]},
  "so_lieu_mau": {"cot": ["Lần", "d' đo (cm)"], "hang": [[n, x] for n, x in enumerate(DO, 1)],
                  "ghi_chu": f"Số liệu minh hoạ: d' = {dp_mh:.2f} cm tính từ mô hình (f = 5 cm, D = 300 cm) cộng sai số đặt giấy {list(LECH)} cm, làm tròn 0,1 cm; chưa phải số đo thật. Trung bình {mean:.2f} cm, G ≈ {G_do:.1f}."},
  "ket_qua_ky_vong": f"Trung bình khoảng {mean:.2f} cm, hơi lớn hơn 5 cm; G ≈ {G_do:.1f}, khớp 5x.",
  "hien_tuong_hay_sai": ["Tưởng khoảng cách đo được đúng bằng f dù đèn ở gần.", "Dùng f tính bằng mét khi tính G = 25/f.",
                         "Đặt giấy ở chỗ ảnh to nhất thay vì rõ nhất."],
  "sai_so_thuong_gap": "Khó xác định chỗ ảnh rõ nhất; đèn chưa đủ xa nên d' hơi lớn hơn f; đọc thước sai lệch vài mm.",
  "an_toan": "Không hứng ảnh Mặt Trời vào mắt hoặc để lâu trên giấy (có thể cháy).",
  "goi_y_mo_phong": {"loai": "2d_dong_hoc+bang_so_lieu", "y_tuong": "Kéo vị trí màn sau thấu kính, ảnh đèn nét nhất ở d'; kéo khoảng cách đèn D để thấy d' tiến về f.",
                     "diem_nhan": "D càng lớn, d' càng gần f; G tính từ f đo được."}})
SOI = [2, 4, 6, 8]
tn.append({**base,
  "id": "tn-l9-kinhlup-02", "ten": "Soi chữ nhỏ trên vỏ hộp sữa bằng kính lúp 2,5x, nâng kính dần lên", "loai": "thi_nghiem", "muc_do": "co_ban",
  "kien_thuc": ["kinhlup.anh_ao", "kinhlup.cach_dung", "thaukinh.anh_theo_vi_tri"],
  "muc_tieu": "Thấy kính lúp chỉ cho ảnh ảo cùng chiều, to hơn khi vật nằm trong khoảng tiêu cự; quá tiêu điểm thì ảnh nhoè rồi lộn ngược.",
  "dung_cu": [{"ten": "Kính lúp ghi 2,5x (f = 10 cm)", "so_luong": 1}, {"ten": "Vỏ hộp sữa có dòng chữ hạn dùng nhỏ", "so_luong": 1},
              {"ten": "Thước kẻ", "so_luong": 1}],
  "cac_buoc": {"lam": ["Đặt kính sát dòng chữ nhỏ trên vỏ hộp sữa, mắt gần kính.", "Nâng kính lên từng 2 cm tới khoảng 10 cm, mắt luôn nhìn qua kính.",
                       "Nâng kính lên 15 cm rồi lùi mắt ra xa kính khoảng 60 cm (ảnh thật ở cách kính 30 cm)."],
               "quan_sat": ["Chữ to dần, cùng chiều.", "Ở gần 10 cm chữ nhoè hẳn.", "Ở 15 cm, mắt ở xa kính: chữ lộn ngược."],
               "rut_ra": ["Kính chỉ phóng to cùng chiều khi vật nằm trong khoảng tiêu cự (ảnh ảo).", "Kính 2,5x có f khoảng 10 cm."]},
  "tham_so": [{"ky_hieu": "d", "ten": "Khoảng cách chữ → kính", "don_vi": "cm", "kieu": "dieu_chinh", "min": 1, "max": 16, "mac_dinh": 6, "buoc": 1},
              {"ky_hieu": "f", "ten": "Tiêu cự", "don_vi": "cm", "kieu": "co_dinh", "gia_tri": 10},
              {"ky_hieu": "d'", "ten": "Vị trí ảnh (âm: ảnh ảo)", "don_vi": "cm", "kieu": "tinh_ra"},
              {"ky_hieu": "k", "ten": "Số phóng đại |d'|/d", "don_vi": "", "kieu": "tinh_ra"}],
  "mo_hinh": {"phuong_trinh": ["1/f = 1/d + 1/d'", "k = |d'|/d"], "gia_thiet": ["thấu kính mỏng", "d' < 0: ảnh ảo cùng phía vật", "d = f không có ảnh: mô phỏng hiện cảnh báo, không tính d', k", "ảnh thật (d > f) chỉ nhìn rõ khi mắt cách ảnh ≥ 25 cm"]},
  "so_lieu_mau": {"cot": ["d (cm)", "d' (cm)", "k"], "hang": [[d, round(img(d, 10)[0], 1), round(img(d, 10)[1], 2)] for d in SOI],
                  "ghi_chu": "Số liệu minh hoạ tính từ mô hình f = 10 cm; thí nghiệm trong bài chỉ quan sát định tính."},
  "ket_qua_ky_vong": "d < 10 cm: ảnh ảo cùng chiều, to dần khi d tăng; gần 10 cm: nhoè; d = 15 cm, mắt cách kính 60 cm: thấy chữ lộn ngược (ảnh thật cách kính 30 cm).",
  "hien_tuong_hay_sai": ["Tưởng kính lúp đặt ở đâu cũng phóng to cùng chiều.", "Tưởng đưa mắt ra xa kính sẽ thấy rộng hơn."],
  "goi_y_mo_phong": {"loai": "2d_dong_hoc", "y_tuong": "Kéo vị trí vật qua F, vẽ hai tia đặc biệt; ảnh ảo nét đứt đổi sang ảnh thật nét liền khi d > f.",
                     "diem_nhan": "Tại d = f hai tia ló song song: không có ảnh (nhoè)."}})
tn.append({**base,
  "id": "tn-l9-kinhlup-03", "ten": "Ảnh ngọn nến qua thấu kính f = 10 cm ở ba vị trí (bài mẫu 1)", "loai": "vi_du", "muc_do": "trung_binh",
  "kien_thuc": ["thaukinh.dung_anh", "thaukinh.anh_theo_vi_tri", "thaukinh.cong_thuc"],
  "muc_tieu": "Dựng ảnh và nêu tính chất ảnh khi d > 2f, f < d < 2f, d < f; ảnh nào hứng được trên tường.",
  "dung_cu": [{"ten": "Kính lúp dùng làm thấu kính hội tụ f = 10 cm", "so_luong": 1}, {"ten": "Ngọn nến cao 6 cm", "so_luong": 1},
              {"ten": "Màn hứng (bức tường hoặc tấm bìa)", "so_luong": 1}],
  "cac_buoc": {"lam": ["Đặt nến vuông góc trục chính, cách thấu kính lần lượt 30 cm, 15 cm, 6 cm.", "Dịch màn tìm ảnh rõ."],
               "quan_sat": ["30 cm: ảnh thật nhỏ, ngược chiều.", "15 cm: ảnh thật lớn, ngược chiều.", "6 cm: không hứng được; nhìn qua kính thấy ảnh cùng chiều lớn."],
               "rut_ra": ["Vị trí vật so với f và 2f quyết định tính chất ảnh.", "Chỉ ảnh thật hứng được trên màn."]},
  "tham_so": [{"ky_hieu": "d", "ten": "Khoảng cách nến → thấu kính", "don_vi": "cm", "kieu": "dieu_chinh", "min": 2, "max": 40, "mac_dinh": 15, "buoc": 1},
              {"ky_hieu": "f", "ten": "Tiêu cự", "don_vi": "cm", "kieu": "co_dinh", "gia_tri": F3},
              {"ky_hieu": "h", "ten": "Chiều cao nến", "don_vi": "cm", "kieu": "co_dinh", "gia_tri": H_NEN},
              {"ky_hieu": "d'", "ten": "Vị trí ảnh", "don_vi": "cm", "kieu": "tinh_ra"},
              {"ky_hieu": "h'", "ten": "Chiều cao ảnh", "don_vi": "cm", "kieu": "tinh_ra"}],
  "mo_hinh": {"phuong_trinh": ["1/f = 1/d + 1/d'", "k = |d'|/d", "h' = k·h"], "gia_thiet": ["thấu kính mỏng", "nến vuông góc trục chính, chân nến trên trục", "d = f không có ảnh: mô phỏng hiện cảnh báo, không tính d', k"]},
  "so_lieu_mau": {"cot": ["d (cm)", "d' (cm)", "h' (cm)"], "hang": [[d, round(i["dp"], 1), round(H_NEN * i["k"], 1)] for d, i in info3],
                  "ghi_chu": "Tính từ mô hình; d' âm là ảnh ảo."},
  "ket_qua_ky_vong": "d = 30: ảnh thật 3 cm; d = 15: ảnh thật 12 cm; d = 6: ảnh ảo 15 cm cùng chiều.",
  "hien_tuong_hay_sai": ["Tưởng ảnh qua thấu kính hội tụ luôn là ảnh thật.", "Vẽ ảnh ảo bằng nét liền.", "Tưởng ảnh ảo hứng được trên màn."],
  "goi_y_mo_phong": {"loai": "2d_dong_hoc", "y_tuong": "Kéo nến dọc trục chính; tia sáng và ảnh cập nhật; vạch F, 2F trên trục.",
                     "diem_nhan": "Ảnh đổi từ thật sang ảo khi nến đi qua F."}})
for dct in tn:
    p = ROOT / "content" / "thi-nghiem" / f"{dct['id']}.json"
    p.write_text(json.dumps(dct, ensure_ascii=False, indent=1), encoding="utf8")

print("ok", len(h), "| hinh2 B'=(%.1f,%.1f)" % (i2["Apx"], i2["Bpy"]), "| tn1 mean=%.2f G=%.2f worst=%s" % (mean, G_do, worst),
      "| h3", [(d, round(i["dp"], 2), round(i["k"], 2)) for d, i in info3])
