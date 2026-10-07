"""Bài 5. Khúc xạ ánh sáng (KHTN 9, lesson_id 83).
Sinh 4 hình SVG + bảng số liệu thí nghiệm + 3 file content/thi-nghiem/tn-l9-khucxa-0N.json,
thay mốc <!--FIGn--> / __...__ trong theory.src.html -> theory.html.
Mọi tia khúc xạ tính bằng n1 sin i = n2 sin r (không ước lượng). Chạy: cd <thư mục bài> && python3 build_figs.py
"""
import json, math, pathlib
from svg_lib import *

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[2]
PHUT = 16          # số phút đọc: lấy từ lint_do_dai.py, làm tròn lên

S_ = lambda d: math.sin(math.radians(d))
ASIN = lambda x: math.degrees(math.asin(x))
def refr(i, n1, n2): return ASIN(n1 * S_(i) / n2)
def vn(x, nd=1):
    """Số thập phân kiểu Việt trong $…$."""
    s = f"{x:.{nd}f}".replace(".", "{,}")
    return s

def P(x, y): return f"{x:.1f},{y:.1f}"
def line(x1, y1, x2, y2, c="currentColor", w=2, dash="", op=1):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{c}" stroke-width="{w}"{d} opacity="{op}"/>'
def ray(x1, y1, x2, y2, c=RED, w=2.6, op=1, at=0.55):
    """Tia sáng: thân liền + đầu V 30° đặt giữa tia, chỉ chiều truyền."""
    mx, my = x1 + (x2 - x1) * at, y1 + (y2 - y1) * at
    g = line(x1, y1, x2, y2, c, w, "", op)
    return g + f'<g opacity="{op}">' + chevron(mx, my, x2 - x1, y2 - y1, c, 2.4, 13) + "</g>"
def normal(x, y1, y2): return line(x, y1, x, y2, "currentColor", 1.6, "6 5", .75)
def sub(base, s): return f'{base}<tspan dy="5" font-size="13">{s}</tspan>'
def arc(cx, cy, r, a1, a2, c="currentColor", w=1.6):
    """Cung tâm (cx,cy), góc toán học a1→a2 (độ, ngược kim đồng hồ, trục y hướng lên)."""
    p1 = (cx + r * math.cos(math.radians(a1)), cy - r * math.sin(math.radians(a1)))
    p2 = (cx + r * math.cos(math.radians(a2)), cy - r * math.sin(math.radians(a2)))
    sweep = 0 if a2 > a1 else 1
    return f'<path d="M{P(*p1)} A{r},{r} 0 0 {sweep} {P(*p2)}" fill="none" stroke="{c}" stroke-width="{w}"/>'
def polar(cx, cy, r, a): return cx + r * math.cos(math.radians(a)), cy - r * math.sin(math.radians(a))
WATER = "rgba(56,189,248,.14)"
GLASS = "rgba(148,163,184,.2)"

# ---------- Hình 1: ống hút trông gãy (chỉ vẽ cảnh, không vẽ đường tia => không lộ đáp án dự đoán)
b = ""
yl = lambda y: 120 + (y - 40) / 240 * 15            # mép trái thành ly
yr = lambda y: 300 - (y - 40) / 240 * 15            # mép phải
b += f'<polygon points="{P(yl(130),130)} {P(yr(130),130)} {P(285,280)} {P(135,280)}" fill="{WATER}"/>'
b += f'<polygon points="{P(120,40)} {P(300,40)} {P(285,280)} {P(135,280)}" fill="none" stroke="currentColor" stroke-width="2.4"/>'
b += line(yl(130), 130, yr(130), 130, BLUE, 2)
b += f'<path d="M305,14 L240,130 L170,200" fill="none" stroke="{ORG}" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/>'
b += text(306, 136, "mặt nước", BLUE, 17, "start", "600")
b += text(318, 34, "ống hút", ORG, 17, "start", "700")
b += text(16, 64, "Trông như", "currentColor", 17, "start", "700")
b += text(16, 86, "gãy ở đây", "currentColor", 17, "start", "700")
b += line(100, 92, 230, 127, "currentColor", 1.5, "4 4", .8)
fig1 = wrap("0 0 420 296", "Ống hút thẳng cắm trong ly nước trông như bị gãy ở mặt nước", b,
            "Hình 1. Nhìn chéo từ trên xuống: ống hút thẳng trông như gãy đúng ở mặt nước.")

# ---------- Hình 2: tên gọi các tia và góc (không khí -> nước, i = 50°, n = 1,33)
n_w = 1.33
i2 = 50; r2 = refr(i2, 1, n_w)
Ix, Iy, L = 210, 170, 150
Sx, Sy = Ix - L * S_(i2), Iy - L * math.cos(math.radians(i2))
Spx = Ix + L * S_(i2)
Rx, Ry = Ix + L * S_(r2), Iy + L * math.cos(math.radians(r2))
b = f'<rect x="10" y="{Iy}" width="400" height="{340 - Iy - 6}" fill="{WATER}"/>'
b += line(10, Iy, 410, Iy, "currentColor", 2.2)
b += normal(Ix, 26, 322)
b += ray(Sx, Sy, Ix, Iy)
b += ray(Ix, Iy, Spx, Sy, RED, 2.2, .45)
b += ray(Ix, Iy, Rx, Ry)
b += arc(Ix, Iy, 46, 90, 90 + i2) + text(*polar(Ix, Iy, 64, 90 + i2 / 2), "i", "currentColor", 18, "middle", "700")
b += arc(Ix, Iy, 46, 90 - i2, 90, "currentColor", 1.2) + text(*polar(Ix, Iy, 64, 90 - i2 / 2), "i'", "currentColor", 17, "middle", "600")
lx, ly = polar(Ix, Iy, 68, 270 + r2 / 2)
b += arc(Ix, Iy, 50, 270, 270 + r2) + text(lx, ly + 10, "r", "currentColor", 18, "middle", "700")
b += text(Sx - 6, Sy - 6, "S", RED, 18, "end", "700")
b += text(Spx + 6, Sy - 6, "S'", RED, 17, "start", "600")
b += text(Rx + 8, Ry + 14, "R", RED, 18, "start", "700")
b += text(Ix - 8, Iy + 22, "I", "currentColor", 18, "end", "700")
b += text(Ix + 8, 40, "N", "currentColor", 18, "start", "700")
b += text(Ix + 8, 330, "N'", "currentColor", 18, "start", "700")
b += text(100, 130, "tia tới", RED, 17, "end", "700")
b += text(272, 236, "tia khúc xạ", RED, 17, "start", "700")
b += text(300, 120, "tia phản xạ", RED, 17, "start", "600")
b += text(16, 160, "Không khí", "currentColor", 17, "start", "600")
b += text(16, 196, "Nước", BLUE, 17, "start", "600")
fig2 = wrap("0 0 420 340", "Tia tới SI, pháp tuyến NN' nét đứt, tia khúc xạ IR, tia phản xạ mờ, góc tới i và góc khúc xạ r", b,
            "Hình 2. Ánh sáng đi từ không khí vào nước. Pháp tuyến NN' vẽ nét đứt; góc tới <em>i</em> và góc khúc xạ <em>r</em> đều đo từ pháp tuyến. Tia phản xạ IS' vẽ mờ.")

# ---------- Hình 3: hai chiều truyền (n thuỷ tinh = 1,5)
n_g = 1.5
b = line(210, 18, 210, 244, "currentColor", 1, "", .35)
panels = ((0, 50, 1, n_g, "Không khí", "Thuỷ tinh", "(a) r &lt; i", "gần pháp tuyến"),
          (210, 35, n_g, 1, "Thuỷ tinh", "Không khí", "(b) r &gt; i", "xa pháp tuyến"))
geo3 = {}
for x0, i, n1, n2, top, bot, cap1, cap2 in panels:
    r = refr(i, n1, n2); geo3[x0] = (i, r)
    cx, cy, L = x0 + 105, 140, 100
    fill_y, fill_h = (cy, 104) if n2 > n1 else (18, cy - 18)
    b += f'<rect x="{x0 + 8}" y="{fill_y}" width="194" height="{fill_h}" fill="{GLASS}"/>'
    b += line(x0 + 8, cy, x0 + 202, cy, "currentColor", 2)
    b += normal(cx, 26, 238)
    sx, sy = cx - L * S_(i), cy - L * math.cos(math.radians(i))
    rx, ry = cx + L * S_(r), cy + L * math.cos(math.radians(r))
    b += ray(sx, sy, cx, cy) + ray(cx, cy, rx, ry)
    b += arc(cx, cy, 40, 90, 90 + i) + text(*polar(cx, cy, 56, 90 + i / 2), "i", "currentColor", 18, "middle", "700")
    lx, ly = polar(cx, cy, 58, 270 + r / 2)
    b += arc(cx, cy, 42, 270, 270 + r) + text(lx, ly + 10, "r", "currentColor", 18, "middle", "700")
    b += text(x0 + 202, 126, top, "currentColor", 17, "end", "600")
    b += text(x0 + 12, 162, bot, "currentColor", 17, "start", "600")
    b += text(x0 + 105, 266, cap1, GRN, 17, "middle", "700")
    b += text(x0 + 105, 286, cap2, GRN, 17, "middle", "600")
fig3 = wrap("0 0 420 294", "Hai chiều truyền: vào thuỷ tinh tia lệch gần pháp tuyến; ra không khí tia lệch xa pháp tuyến", b,
            f"Hình 3. (a) Không khí → thuỷ tinh, <em>i</em> = {geo3[0][0]}°, <em>r</em> ≈ {geo3[0][1]:.0f}°. "
            f"(b) Thuỷ tinh → không khí, <em>i</em> = {geo3[210][0]}°, <em>r</em> ≈ {geo3[210][1]:.0f}°. Vùng tô xám là thuỷ tinh.")

# ---------- Hình 4: ảnh viên sỏi dưới đáy nước nằm cao hơn vật (n = 1,33)
Ox, Oy, ys, ytop = 120, 270, 110, 50
b = f'<rect x="10" y="{ys}" width="400" height="{292 - ys}" fill="{WATER}"/>'
b += line(10, ys, 410, ys, "currentColor", 2.2) + line(10, 292, 410, 292, "currentColor", 2.4)
hits, dirs = [], []
RW4 = (0, 20)
for rw in RW4:
    hx = Ox + (Oy - ys) * math.tan(math.radians(rw))
    a = refr(rw, n_w, 1)
    ex = hx + (ys - ytop) * math.tan(math.radians(a))
    b += ray(Ox, Oy, hx, ys, RED, 2.4) + ray(hx, ys, ex, ytop, RED, 2.4)
    hits.append((hx, ys)); dirs.append((-S_(a), math.cos(math.radians(a))))
# giao điểm hai đường kéo dài ngược
(x1, y1), (x2, y2) = hits; (d1x, d1y), (d2x, d2y) = dirs
det = d1x * (-d2y) - d1y * (-d2x)
t = ((x2 - x1) * (-d2y) - (y2 - y1) * (-d2x)) / det
Ix4, Iy4 = x1 + t * d1x, y1 + t * d1y
assert ys < Iy4 < Oy and Ix4 >= Ox - 0.5, (Ix4, Iy4)      # ảnh cao hơn vật và lệch về phía mắt
for hx, hy in hits:
    b += line(hx, hy, Ix4, Iy4, BLUE, 2, "6 5", .95)
b += normal(hits[1][0], 66, 160)
b += f'<circle cx="{Ox}" cy="{Oy}" r="7" fill="{ORG}" stroke="currentColor" stroke-width="1.6"/>'
b += f'<circle cx="{Ix4:.1f}" cy="{Iy4:.1f}" r="7" fill="none" stroke="{BLUE}" stroke-width="2.2" stroke-dasharray="3 3"/>'
ex0 = sum(hx + (ys - ytop) * math.tan(math.radians(refr(rw, n_w, 1))) for (hx, _), rw in zip(hits, RW4)) / 2
b += f'<path d="M{ex0 - 40:.1f},{ytop - 12} Q{ex0:.1f},{ytop - 40} {ex0 + 40:.1f},{ytop - 12} Q{ex0:.1f},{ytop + 16} {ex0 - 40:.1f},{ytop - 12} Z" fill="none" stroke="currentColor" stroke-width="2"/>'
b += f'<circle cx="{ex0:.1f}" cy="{ytop - 12}" r="6" fill="currentColor"/>'
b += text(ex0 + 48, ytop - 6, "mắt", "currentColor", 17, "start", "700")
b += text(Ox - 12, Oy + 6, "sỏi thật", ORG, 17, "end", "700")
b += text(Ix4 - 12, Iy4 - 6, "ảnh", BLUE, 17, "end", "700")
b += text(Ix4 - 12, Iy4 + 14, "(mắt thấy)", BLUE, 17, "end", "600")
b += text(16, ys - 12, "Không khí", "currentColor", 17, "start", "600")
b += text(16, ys + 26, "Nước", BLUE, 17, "start", "600")
TILE4 = f"{(Iy4 - ys) / (Oy - ys):.1f}".replace(".", ",")
fig4 = wrap("0 0 420 300", "Hai tia từ viên sỏi khúc xạ ở mặt nước; kéo dài ngược hai tia vào mắt gặp nhau tại ảnh nằm cao hơn viên sỏi", b,
            f"Hình 4. Tia thẳng đứng đi thẳng; tia xiên lệch xa pháp tuyến khi ra không khí. Kéo dài ngược (nét đứt xanh) gặp nhau ở <strong>ảnh</strong>, ở khoảng {TILE4} độ sâu thật. Nhìn càng xiên, ảnh càng nổi cao.")

# ---------- Bảng số liệu thí nghiệm 2 (số liệu minh hoạ từ mô hình n = 1,5, đọc tròn tới 1°)
ANG = (20, 35, 50, 65, 80)
rows = []
for i in ANG:
    r_true = refr(i, 1, n_g); r_doc = round(r_true)
    rows.append((i, r_true, r_doc, S_(i) / S_(r_doc)))
ratios = [q for *_, q in rows]
mean = sum(ratios) / len(ratios)
dev = [abs(q - n_g) for q in ratios]
mx = max(dev)
worst = [rw for rw, d in zip(rows, dev) if abs(d - mx) < 1e-6]
assert len(worst) == 1
wi, wrt, wrd, wq = worst[0]
bang = "\n".join(f"<tr><td>$i = {i}^\\circ$, $r = {rd}^\\circ$</td><td>${vn(q, 2)}$</td></tr>" for i, _, rd, q in rows)
nx = (f"trung bình ${vn(mean, 2)}$, rất gần $n = 1{{,}}5$. Lệch nhiều nhất là lần $i = {wi}^\\circ$ "
      f"(tỉ số ${vn(wq, 2)}$): góc thật khoảng ${vn(wrt, 1)}^\\circ$ nhưng chỉ đọc được ${wrd}^\\circ$ vì vạch chia $1^\\circ$. "
      f"Sai số chủ yếu do đọc góc và tia laser có bề rộng; muốn chính xác hơn, đo nhiều lần rồi lấy trung bình.")

h = (HERE / "theory.src.html").read_text(encoding="utf8")
h = h.replace("__GOC_TN2__", ", ".join(f"{a}^\\circ" for a in ANG)).replace("__BANG_TN2__", bang).replace("__NHAN_XET_TN2__", nx).replace("__PHUT__", str(PHUT))
for n, f in enumerate((fig1, fig2, fig3, fig4), 1):
    assert f"<!--FIG{n}-->" in h, n
    h = h.replace(f"<!--FIG{n}-->", f)
assert "__" not in h.replace("___", "")
(HERE / "theory.html").write_text(h, encoding="utf8")

# ---------- Kho thí nghiệm
BAI = "Bài 5. Khúc xạ ánh sáng"
SRC = "content/lesson-samples/l9-khuc-xa-anh-sang/theory.html"
base = {"mon": "vat-ly", "lop": 9, "bai": BAI, "lesson_id": 83, "nguon_trong_bai": SRC}
tn = []
tn.append({**base,
  "id": "tn-l9-khucxa-01", "ten": "Tia laser đi từ không khí vào bể nước có pha sữa", "loai": "thi_nghiem", "muc_do": "co_ban",
  "kien_thuc": ["khucxa.hien_tuong", "khucxa.phan_xa_kem_theo"],
  "muc_tieu": "Thấy tận mắt tia sáng gãy khúc ở mặt nước khi chiếu xiên, và một phần ánh sáng bị phản xạ.",
  "dung_cu": [{"ten": "Bể kính (hoặc hộp nhựa trong) đựng nước", "so_luong": 1},
              {"ten": "Bút laser đỏ công suất thấp", "so_luong": 1},
              {"ten": "Vài giọt sữa, que hương và bật lửa", "so_luong": 1}],
  "cac_buoc": {"lam": ["Pha vài giọt sữa vào nước cho thấy vệt sáng.", "Đốt que hương cho khói bay sát trên mặt nước.",
                       "Chiếu laser xiên xuống mặt nước, đổi dần góc chiếu; chiếu thêm một lần vuông góc."],
               "quan_sat": ["Vệt sáng trong khói và trong nước không thẳng hàng: tia gãy ở mặt nước.",
                            "Một vệt mờ hắt ngược lên khói (phản xạ).", "Chiếu vuông góc thì tia đi thẳng."],
               "rut_ra": ["Ánh sáng đổi phương khi truyền xiên qua mặt phân cách hai môi trường trong suốt (khúc xạ).",
                          "Tia khúc xạ trong nước lệch gần pháp tuyến hơn tia tới.", "i = 0 thì r = 0."]},
  "tham_so": [{"ky_hieu": "i", "ten": "Góc tới", "don_vi": "độ", "kieu": "dieu_chinh", "min": 0, "max": 85, "mac_dinh": 45, "buoc": 5},
              {"ky_hieu": "n1", "ten": "Chiết suất không khí", "don_vi": "", "kieu": "co_dinh", "gia_tri": 1},
              {"ky_hieu": "n2", "ten": "Chiết suất nước", "don_vi": "", "kieu": "co_dinh", "gia_tri": 1.33},
              {"ky_hieu": "r", "ten": "Góc khúc xạ", "don_vi": "độ", "kieu": "tinh_ra"}],
  "mo_hinh": {"phuong_trinh": ["n1·sin(i) = n2·sin(r)", "i' = i (tia phản xạ)"],
              "gia_thiet": ["mặt nước phẳng, nằm yên", "ánh sáng đơn sắc đỏ"]},
  "so_lieu_mau": {"cot": ["i (độ)", "r (độ)"],
                  "hang": [[i, round(refr(i, 1, n_w), 1)] for i in (0, 20, 40, 60, 80)],
                  "ghi_chu": "Số liệu minh hoạ tính từ mô hình n = 1,33; thí nghiệm này chỉ quan sát định tính."},
  "ket_qua_ky_vong": "Tia trong nước gãy về phía pháp tuyến; góc tới càng lớn, tia càng gãy rõ; chiếu vuông góc thì không gãy.",
  "hien_tuong_hay_sai": ["Tưởng chiếu vuông góc thì tia cũng gãy.", "Đo góc từ mặt nước thay vì từ pháp tuyến.",
                         "Tưởng toàn bộ ánh sáng đi vào nước, không có phần phản xạ."],
  "an_toan": "Không chiếu laser vào mắt; dùng bút laser công suất thấp.",
  "goi_y_mo_phong": {"loai": "2d_dong_hoc", "y_tuong": "Kéo thanh trượt góc tới, tia khúc xạ và tia phản xạ mờ cập nhật theo định luật.",
                     "diem_nhan": "Tại i = 0 tia đi thẳng; tia khúc xạ luôn ở bên kia pháp tuyến."}})
tn.append({**base,
  "id": "tn-l9-khucxa-02", "ten": "Đo góc khúc xạ qua khối nhựa bán trụ trên đĩa chia độ", "loai": "thi_nghiem", "muc_do": "trung_binh",
  "kien_thuc": ["khucxa.dinh_luat", "khucxa.chiet_suat"],
  "muc_tieu": "Từ số đo i và r, thấy tỉ số sin i / sin r gần như không đổi và bằng chiết suất của nhựa.",
  "dung_cu": [{"ten": "Khối nhựa trong hình bán trụ", "so_luong": 1},
              {"ten": "Đĩa chia độ tròn, vạch 1°", "so_luong": 1},
              {"ten": "Bút laser (hoặc đèn chiếu khe hẹp)", "so_luong": 1}],
  "cac_buoc": {"lam": ["Đặt mặt phẳng của khối bán trụ đi qua tâm đĩa, vuông góc đường 0°.",
                       "Chiếu tia laser từ không khí vào đúng tâm với i = " + ", ".join(f"{i}°" for i in ANG) + ".",
                       "Đọc góc khúc xạ r trên đĩa ở mỗi lần."],
               "quan_sat": ["r luôn nhỏ hơn i; i tăng thì r tăng.", "Tia ló ra khỏi mặt cong không gãy thêm."],
               "rut_ra": ["sin i / sin r gần như không đổi: đó là chiết suất của nhựa so với không khí.",
                          "Sai lệch do đọc góc tới 1°; góc nhỏ thì sai lệch tương đối lớn hơn."]},
  "tham_so": [{"ky_hieu": "i", "ten": "Góc tới", "don_vi": "độ", "kieu": "dieu_chinh", "min": 0, "max": 80, "mac_dinh": 45, "buoc": 15},
              {"ky_hieu": "n", "ten": "Chiết suất nhựa", "don_vi": "", "kieu": "co_dinh", "gia_tri": n_g},
              {"ky_hieu": "r", "ten": "Góc khúc xạ đọc được", "don_vi": "độ", "kieu": "do_duoc", "sai_so_do": 0.5},
              {"ky_hieu": "q", "ten": "Tỉ số sin i / sin r", "don_vi": "", "kieu": "tinh_ra"}],
  "mo_hinh": {"phuong_trinh": ["sin(i) = n·sin(r)", "q = sin(i)/sin(r)"],
              "gia_thiet": ["tia tới đi đúng tâm đĩa", "mặt cong: tia đi theo bán kính nên không gãy", "đọc góc làm tròn tới 1°"]},
  "so_lieu_mau": {"cot": ["i (độ)", "r đọc (độ)", "sin i / sin r"],
                  "hang": [[i, rd, round(q, 2)] for i, _, rd, q in rows],
                  "ghi_chu": f"Số liệu minh hoạ: r tính từ n = 1,5 rồi làm tròn tới 1°, chưa phải số đo thật. Trung bình tỉ số {mean:.2f}."},
  "ket_qua_ky_vong": f"Tỉ số trung bình khoảng {mean:.2f}, khớp n = 1,5 trong sai số đọc góc.",
  "hien_tuong_hay_sai": ["Tính i / r thay cho sin i / sin r.", "Đọc r từ mặt phẳng của khối thay vì từ pháp tuyến."],
  "sai_so_thuong_gap": "Vạch chia 1°, tia laser có bề rộng, tia không đi đúng tâm đĩa.",
  "goi_y_mo_phong": {"loai": "so_do_luc+bang_so_lieu", "y_tuong": "Xoay đèn quanh tâm đĩa, đọc r, bảng tự điền sin i / sin r.",
                     "diem_nhan": "i / r thay đổi nhiều, sin i / sin r gần như đứng yên."}})
tn.append({**base,
  "id": "tn-l9-khucxa-03", "ten": "Đồng xu hiện ra khi rót nước vào bát", "loai": "thi_nghiem", "muc_do": "co_ban",
  "kien_thuc": ["khucxa.anh_qua_mat_phan_cach"],
  "muc_tieu": "Thấy ảnh của vật dưới nước nằm cao hơn vật thật do khúc xạ.",
  "dung_cu": [{"ten": "Bát sứ không trong suốt", "so_luong": 1}, {"ten": "Đồng xu", "so_luong": 1}, {"ten": "Bình nước", "so_luong": 1}],
  "cac_buoc": {"lam": ["Đặt đồng xu dưới đáy bát.", "Lùi đầu tới khi thành bát vừa che khuất đồng xu; giữ yên mắt.",
                       "Một bạn rót nước từ từ vào bát."],
               "quan_sat": ["Đồng xu hiện ra dù mắt và bát không di chuyển."],
               "rut_ra": ["Tia từ đồng xu ra không khí lệch xa pháp tuyến, đi qua mép bát tới mắt.",
                          "Mắt thấy ảnh đồng xu nằm cao hơn vị trí thật."]},
  "tham_so": [{"ky_hieu": "h", "ten": "Độ sâu nước", "don_vi": "cm", "kieu": "dieu_chinh", "min": 0, "max": 8, "mac_dinh": 6, "buoc": 1},
              {"ky_hieu": "n", "ten": "Chiết suất nước", "don_vi": "", "kieu": "co_dinh", "gia_tri": 1.33},
              {"ky_hieu": "h_anh", "ten": "Độ sâu ảnh khi nhìn gần thẳng đứng", "don_vi": "cm", "kieu": "tinh_ra"}],
  "mo_hinh": {"phuong_trinh": ["n·sin(r_nuoc) = sin(r_khong_khi)", "h_anh ≈ h / n (nhìn gần thẳng đứng)"],
              "gia_thiet": ["mặt nước phẳng", "mắt cố định"]},
  "so_lieu_mau": {"cot": ["h (cm)", "h_anh (cm)"], "hang": [[h_, round(h_ / n_w, 1)] for h_ in (2, 4, 6, 8)],
                  "ghi_chu": "Số liệu minh hoạ tính từ h_anh ≈ h / 1,33, chỉ đúng khi nhìn gần thẳng đứng."},
  "ket_qua_ky_vong": "Đồng xu hiện ra khi mực nước đủ cao; ảnh nằm cao hơn đáy bát.",
  "hien_tuong_hay_sai": ["Tưởng đồng xu bị nước đẩy nổi lên.", "Tưởng thấy vật dưới nước ở đâu thì vật nằm đúng chỗ đó."],
  "goi_y_mo_phong": {"loai": "2d_dong_hoc", "y_tuong": "Kéo mực nước, vẽ tia từ đồng xu qua mép bát tới mắt và ảnh nét đứt.",
                     "diem_nhan": "Ảnh nổi lên khi nước dâng; mắt không cần di chuyển."}})
for d in tn:
    p = ROOT / "content" / "thi-nghiem" / f"{d['id']}.json"
    p.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf8")

print("ok", len(h), "| r2=%.2f" % r2, "| anh hinh4 =(%.1f, %.1f)" % (Ix4, Iy4), "| tn2 mean=%.3f worst i=%d" % (mean, wi))
