"""Sinh 3 hình SVG + bảng số liệu thí nghiệm cho bài 'Làm quen với Vật lí' (lesson 46),
thay mốc <!--FIGn-->, __BANG_TN2__, __NS__, __TS__, __G__, __CHENH__, __PHUT__ trong theory.src.html -> theory.html,
và ghi 3 file thí nghiệm content/thi-nghiem/tn-l10-lam-quen-0{1,2,3}.json (số liệu tính từ cùng mô hình).
Có lớp kiểm hình học: hộp nhãn không chồng nhau, không vượt viewBox, chữ nằm gọn trong hộp.
Chạy: python3 build_figs.py   (sau đó: python3 build_bundle.py)"""
import json, math, pathlib, re, subprocess, sys
from svg_lib import RED, BLUE, ORG, GRN, wrap

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[2]
COL = {"r": RED, "b": BLUE, "o": ORG, "g": GRN, "k": "currentColor"}


def vn(x, nd=2):
    return f"{x:.{nd}f}".replace(".", "{,}")


def vp(x, nd=2):  # số thập phân ngoài $…$: dấu phẩy
    return f"{x:.{nd}f}".replace(".", ",")


class Canvas:
    def __init__(self, name, w, h):
        self.name, self.w, self.h = name, w, h
        self.body, self.labels, self.markers, self.arrows, self.boxes = "", [], set(), {}, []

    def line(self, x1, y1, x2, y2, c="currentColor", w=2, dash="", op=1):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.body += f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{c}" stroke-width="{w}"{d} opacity="{op}"/>'

    def arr(self, tag, c, x1, y1, x2, y2, w=3, head=11):
        L = math.hypot(x2 - x1, y2 - y1)
        ux, uy = (x2 - x1) / L, (y2 - y1) / L
        ex, ey = x2 - ux * head, y2 - uy * head
        self.markers.add((c, head))
        self.body += (f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{ex:.1f}" y2="{ey:.1f}" stroke="{COL[c]}" stroke-width="{w}" '
                      f'marker-end="url(#{self.name}-{c}{head})"/>')
        self.arrows[tag] = (x1, y1, x2, y2)

    def text(self, x, y, s, c="currentColor", size=14, anchor="start", weight="700", box=None):
        self.body += f'<text x="{x:.1f}" y="{y:.1f}" fill="{c}" font-size="{size}" font-weight="{weight}" text-anchor="{anchor}">{s}</text>'
        plain = re.sub(r"<[^>]+>", "", s)
        wdt = 0.58 * size * len(plain)
        x0 = x if anchor == "start" else (x - wdt / 2 if anchor == "middle" else x - wdt)
        self.labels.append((plain, x0, y - 0.78 * size, x0 + wdt, y + 0.22 * size, size))
        if box:  # chữ phải nằm gọn trong hộp (x, y, w, h)
            bx, by, bw, bh = box
            if x0 < bx + 6 or x0 + wdt > bx + bw - 6 or y - 0.78 * size < by or y + 0.22 * size > by + bh:
                ERR.append(f"{self.name}: chữ '{plain}' không nằm gọn trong hộp {box} (rộng chữ {wdt:.0f})")

    def rect(self, x, y, w, h, stroke, fill, r=10, sw=2.5):
        self.body += f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'

    def defs(self):
        out = "<defs>"
        for c, hd in sorted(self.markers):
            out += (f'<marker id="{self.name}-{c}{hd}" viewBox="0 0 10 10" refX="0" refY="5" markerWidth="{hd}" markerHeight="{hd}" '
                    f'markerUnits="userSpaceOnUse" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="{COL[c]}"/></marker>')
        return out + "</defs>"

    def check(self):
        errs = []
        for i, a in enumerate(self.labels):
            if a[5] < 14:
                errs.append(f"{self.name}: nhãn '{a[0]}' cỡ {a[5]} < 14")
            if a[1] < 2 or a[3] > self.w - 2 or a[2] < 0 or a[4] > self.h:
                errs.append(f"{self.name}: nhãn '{a[0]}' vượt viewBox {a[1:5]}")
            for b in self.labels[i + 1:]:
                if a[1] < b[3] and b[1] < a[3] and a[2] < b[4] and b[2] < a[4]:
                    errs.append(f"{self.name}: nhãn '{a[0]}' chồng '{b[0]}'")
        return errs

    def svg(self, label, cap):
        return wrap(f"0 0 {self.w} {self.h}", label, self.defs() + self.body, cap)


ERR = []
G = 9.8

# ================= Mô hình số liệu TN2 (sách và giấy rơi 2 m, video 60 hình/s)
H, FPS = 2.0, 60
T_SACH = math.sqrt(2 * H / G)                      # rơi tự do, bỏ cản không khí
K_VO = 1.07                                        # GIẢ ĐỊNH minh hoạ: cản không khí làm giấy vo chậm hơn 7 %
T_VO = T_SACH * K_VO
PHASE = (0.0, 0.4, 0.8)                            # thời điểm buông lệch so với khung hình (phần khung)
FR_SACH = [math.floor(T_SACH * FPS + p) for p in PHASE]
FR_VO = [math.floor(T_VO * FPS + p) for p in PHASE]
assert FR_SACH == [38, 38, 39] and FR_VO == [41, 41, 41], (FR_SACH, FR_VO)   # khớp quiz Câu 6
MEAN_S, MEAN_V = sum(FR_SACH) / 3, sum(FR_VO) / 3
TS, TV = MEAN_S / FPS, MEAN_V / FPS
G_TINH = 2 * H / TS ** 2
assert abs(G_TINH - 9.8) < 0.05 and round(4 / 0.64 ** 2, 1) == 9.8
CHENH = MEAN_V - MEAN_S
assert 2.6 < CHENH < 2.8 and CHENH > 1 and (max(FR_SACH) - min(FR_SACH)) <= 1       # "gần 3" và > sai số ±1
assert round(TS, 2) == 0.64 and round(TV, 2) == 0.68
SAI_SO_S = 1 / FPS
assert abs(SAI_SO_S - 0.017) < 5e-4

# TN3: robot hút bụi đi hình vuông cạnh 1,5 m, 0,2 m/s, 4 góc, mỗi góc mất 0,75 s khi rẽ.
L_CNC, V_CNC, N_GOC, T_GOC = 6.0, 0.2, 4, 0.75
T_LT = round(L_CNC / V_CNC, 6)
T_DO = T_LT + N_GOC * T_GOC
assert T_LT == 30 and T_DO == 33 and abs((T_DO - T_LT) / T_LT - 0.10) < 1e-9     # "lệch 10 %"
# thử thách ⭐⭐: 9 m, 0,25 m/s, đo 39 s, 0,75 s/góc
T2 = 9 / 0.25
assert T2 == 36 and (39 - T2) / 0.75 == 4

# ================= Hình 1: thang cấp độ từ vi mô tới vĩ mô
c = Canvas("f1", 420, 215)
XS_ = [58, 160, 262, 364]
YI = 66
# 1) phân tử H2O: O to, hai H nhỏ
c.body += f'<circle cx="{XS_[0]}" cy="{YI}" r="13" fill="{RED}" stroke="currentColor" stroke-width="1.5"/>'
for dx in (-17, 17):
    c.body += f'<circle cx="{XS_[0] + dx}" cy="{YI + 14}" r="7" fill="{BLUE}" stroke="currentColor" stroke-width="1.5"/>'
# 2) giọt nước
x2 = XS_[1]
c.body += (f'<path d="M{x2},{YI - 24} C{x2 + 6},{YI - 8} {x2 + 20},{YI + 4} {x2 + 20},{YI + 16} '
           f'A20,20 0 0 1 {x2 - 20},{YI + 16} C{x2 - 20},{YI + 4} {x2 - 6},{YI - 8} {x2},{YI - 24} Z" fill="rgba(56,189,248,.35)" stroke="{BLUE}" stroke-width="2.5"/>')
# 3) Trái Đất
x3 = XS_[2]
c.body += f'<circle cx="{x3}" cy="{YI}" r="30" fill="rgba(56,189,248,.25)" stroke="{BLUE}" stroke-width="2.5"/>'
c.body += f'<path d="M{x3 - 18},{YI - 12} q10,-6 16,2 q-2,10 -10,10 q-8,0 -6,-12 Z M{x3 + 6},{YI + 8} q12,-4 14,6 q-6,10 -14,2 Z" fill="{GRN}" opacity=".8"/>'
# 4) vũ trụ: thiên hà elip + sao
x4 = XS_[3]
c.body += f'<ellipse cx="{x4}" cy="{YI}" rx="40" ry="16" fill="rgba(251,146,60,.2)" stroke="{ORG}" stroke-width="2.5" transform="rotate(-18 {x4} {YI})"/>'
for dx, dy in ((-34, -20), (30, -24), (-38, 18), (36, 22), (6, -30), (-8, 30)):
    c.body += f'<circle cx="{x4 + dx}" cy="{YI + dy}" r="2.2" fill="currentColor"/>'
NAMES = [("Phân tử,", "nguyên tử"), ("Giọt nước", ""), ("Trái Đất", ""), ("Vũ trụ", "")]
for x, (a, b) in zip(XS_, NAMES):
    c.text(x, 128, a, size=14, anchor="middle")
    if b:
        c.text(x, 146, b, size=14, anchor="middle")
# ngoặc Vi mô / Vĩ mô
YB = 166
c.line(14, YB, 104, YB, ORG, 3)
c.line(14, YB - 6, 14, YB, ORG, 3); c.line(104, YB - 6, 104, YB, ORG, 3)
c.text(59, 192, "Vi mô", ORG, 16, "middle")
c.line(116, YB, 408, YB, BLUE, 3)
c.line(116, YB - 6, 116, YB, BLUE, 3); c.line(408, YB - 6, 408, YB, BLUE, 3)
c.text(262, 192, "Vĩ mô", BLUE, 16, "middle")
# kiểm: biểu tượng không chạm nhãn, bốn trạm cách đều, ngoặc vi mô bao đúng trạm 1 và vĩ mô bao trạm 2-4
ERR += [] if all(14 < XS_[0] < 104 and 116 < x < 408 for x in XS_[1:]) else ["f1: ngoặc không bao đúng trạm"]
ERR += [] if len({XS_[i + 1] - XS_[i] for i in range(3)}) == 1 or max(XS_[i + 1] - XS_[i] for i in range(3)) == 102 else ["f1: trạm không đều"]
fig1 = c.svg("Bốn mức từ nhỏ tới lớn: phân tử và nguyên tử, giọt nước, Trái Đất, vũ trụ; phân tử và nguyên tử thuộc cấp độ vi mô, ba mức còn lại thuộc cấp độ vĩ mô",
             "Hình 1. Vật lí nghiên cứu ở mọi cấp độ, từ vi mô (nguyên tử, phân tử) tới vĩ mô (vật quan sát được bằng mắt thường, Trái Đất, vũ trụ). Hình không theo tỉ lệ.")
ERR += c.check()

# ================= Hình 2: quy trình 5 bước, vòng lặp khi kiểm tra không khớp
c = Canvas("f2", 420, 335)
BX, BW, BH = 190, 222, 38
STEPS = ["1. Quan sát, suy luận", "2. Đề xuất vấn đề", "3. Hình thành giả thuyết", "4. Kiểm tra giả thuyết", "5. Rút ra kết luận"]
YS = [10 + 66 * i for i in range(5)]
for i, (s, y) in enumerate(zip(STEPS, YS)):
    c.rect(BX, y, BW, BH, GRN if i == 4 else BLUE, "rgba(52,211,153,.18)" if i == 4 else "rgba(56,189,248,.16)")
    c.text(BX + BW / 2, y + 25, s, size=14, anchor="middle", box=(BX, y, BW, BH))
    if i < 4:
        c.arr(f"d{i}", "k", BX + BW / 2, y + BH, BX + BW / 2, YS[i + 1], 2, 10)
c.text(BX + BW / 2 + 12, YS[3] + BH + 20, "khớp", GRN, 14)
LX, LW, LH = 8, 160, 64
LY = YS[3] + BH / 2 - LH / 2
c.rect(LX, LY, LW, LH, ORG, "rgba(251,146,60,.16)")
for k, s in enumerate(("Không khớp:", "điều chỉnh hoặc", "bác bỏ giả thuyết")):
    c.text(LX + LW / 2, LY + 20 + 17 * k, s, size=14, anchor="middle", box=(LX, LY, LW, LH))
c.arr("loopL", "o", BX, YS[3] + BH / 2, LX + LW + 3, YS[3] + BH / 2, 2.5, 10)
c.line(LX + LW / 2, LY, LX + LW / 2, YS[2] + BH / 2, ORG, 2.5)
c.arr("loopU", "o", LX + LW / 2, YS[2] + BH / 2, BX - 2, YS[2] + BH / 2, 2.5, 10)
# kiểm: vòng lặp đi từ bước 4 trở lại ĐÚNG bước 3 (cùng độ cao tâm hộp 3), mũi tên xuống đi từ trên xuống
ERR += [] if abs(c.arrows["loopU"][1] - (YS[2] + BH / 2)) < 1e-6 and c.arrows["loopU"][2] == BX - 2 else ["f2: vòng lặp không tới bước 3"]
ERR += [] if all(c.arrows[f"d{i}"][3] > c.arrows[f"d{i}"][1] for i in range(4)) else ["f2: mũi tên bước sai chiều"]
fig2 = c.svg("Sơ đồ năm bước nghiên cứu: quan sát và suy luận, đề xuất vấn đề, hình thành giả thuyết, kiểm tra giả thuyết, rút ra kết luận; nếu kiểm tra không khớp thì điều chỉnh hoặc bác bỏ giả thuyết và quay lại bước hình thành giả thuyết",
             "Hình 2. Quy trình nghiên cứu khoa học. Kiểm tra không khớp thì điều chỉnh hoặc bác bỏ giả thuyết, rồi quay lại bước 3.")
ERR += c.check()

# ================= Hình 3: ảnh chụp cùng lúc t = 0,4 s của ba kiểu thả
TSNAP, SCALE = 0.4, 75.0          # px / m
Y0 = 44
d_book = 0.5 * G * TSNAP ** 2
d_flat = 0.40                      # GIẢ ĐỊNH minh hoạ (giấy phẳng chịu cản lớn)
d_vo = 0.5 * G * (TSNAP / K_VO) ** 2
FLOOR = Y0 + H * SCALE + 12
c = Canvas("f3", 420, 262)
c.text(210, 20, "Ảnh chụp cùng lúc t = 0,4 s (minh hoạ)", size=14, anchor="middle")
c.line(8, Y0, 412, Y0, "currentColor", 1.5, "5 4", .55)
c.text(8, Y0 - 6, "lúc buông", size=14, weight="600")
c.line(8, FLOOR, 412, FLOOR, "currentColor", 3)
COLX = [70, 210, 350]
yb = lambda d: Y0 + d * SCALE
def book(cx, d):
    c.body += f'<rect x="{cx - 20}" y="{yb(d):.1f}" width="40" height="12" rx="2" fill="rgba(251,146,60,.4)" stroke="{ORG}" stroke-width="2.5"/>'
def flat(cx, d):
    c.body += f'<rect x="{cx - 18}" y="{yb(d):.1f}" width="36" height="3" fill="currentColor"/>'
# (a) thả riêng
book(COLX[0] - 24, d_book); flat(COLX[0] + 26, d_flat)
# (b) giấy nằm trên sách
book(COLX[1], d_book); flat(COLX[1], d_book - 3 / SCALE)
# (c) giấy vo tròn cạnh sách
book(COLX[2] - 24, d_book)
c.body += f'<circle cx="{COLX[2] + 26}" cy="{yb(d_vo) + 7:.1f}" r="7" fill="rgba(56,189,248,.35)" stroke="{BLUE}" stroke-width="2.5"/>'
CAP = [("Thả riêng:", "sách tới trước"), ("Giấy nằm trên", "sách: cùng rơi"), ("Giấy vo tròn:", "chỉ chậm chút")]
for x, (a, b) in zip(COLX, CAP):
    c.text(x, 232, a, size=14, anchor="middle")
    c.text(x, 250, b, size=14, anchor="middle")
# kiểm: (a) giấy phẳng cao hơn (y nhỏ hơn) sách nhiều; (b) cùng độ cao; (c) giấy vo chậm hơn sách nhưng chênh < 10 px
ERR += [] if yb(d_flat) < yb(d_book) - 20 else ["f3: (a) giấy phẳng phải ở cao hơn sách rõ rệt"]
ERR += [] if 0 < yb(d_book) - yb(d_vo) < 10 else [f"f3: (c) giấy vo phải cao hơn sách một chút, chênh {(yb(d_book) - yb(d_vo)):.1f}px"]
ERR += [] if yb(d_book) + 12 < FLOOR else ["f3: sách chạm sàn trước thời điểm chụp"]
fig3 = c.svg("Ba kiểu thả chụp cùng lúc giữa chừng: thả riêng thì sách ở thấp hơn tờ giấy phẳng; giấy đặt trên sách thì hai vật cùng độ cao; giấy vo tròn thì chỉ cao hơn sách một chút",
             "Hình 3. Thả từ cùng độ cao, chụp cùng thời điểm (số liệu minh hoạ): giấy phẳng tụt lại vì không khí cản; giấy trên sách rơi cùng sách; giấy vo tròn gần bằng sách.")
ERR += c.check()

if ERR:
    print("\n".join("✗ " + e for e in ERR)); sys.exit(1)

# ================= Bảng số liệu TN2 và các chỗ điền khác
bang = ('<div class="table-scroll">\n<table class="tl-table">\n<thead>\n'
        '<tr><th>Vật (rơi $2\\ \\text{m}$)</th><th>Số khung hình</th><th>$t$ (s)</th></tr>\n</thead>\n<tbody>\n'
        f"<tr><td>Sách</td><td>{' · '.join(map(str, FR_SACH))}</td><td>{vp(TS)}</td></tr>\n"
        f"<tr><td>Giấy vo tròn</td><td>{' · '.join(map(str, FR_VO))}</td><td>{vp(TV)}</td></tr>\n"
        "</tbody>\n</table>\n</div>")
h = (HERE / "theory.src.html").read_text(encoding="utf8")
for n, fg in enumerate((fig1, fig2, fig3), 1):
    assert f"<!--FIG{n}-->" in h, n
    h = h.replace(f"<!--FIG{n}-->", fg)
h = (h.replace("__BANG_TN2__", bang).replace("__NS__", vn(MEAN_S, 1)).replace("__TS__", vn(TS))
      .replace("__G__", vn(G_TINH, 1)).replace("__CHENH__", f"${vn(CHENH, 1)}$"))
assert "__" not in h.replace("__PHUT__", "")
tmp = HERE / ".theory.tmp.html"
tmp.write_text(h.replace("__PHUT__", "15"), encoding="utf8")
lint = ROOT / ".claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts/lint_do_dai.py"
out = subprocess.run([sys.executable, str(lint), str(tmp)], capture_output=True, text=True).stdout
tmp.unlink()
m = re.search(r"~?(\d+(?:[.,]\d+)?)\s*phút", out)
phut = round(float(m.group(1).replace(",", "."))) if m else None
if phut is None:
    print("! không đọc được số phút từ lint_do_dai:\n" + out[:600]); sys.exit(1)
h = h.replace("__PHUT__", str(phut))
(HERE / "theory.html").write_text(h, encoding="utf8")

# ================= File thí nghiệm
BASE = {"mon": "vat-ly", "lop": 10, "bai": "Bài 1. Làm quen với Vật lí", "lesson_id": 46,
        "nguon_trong_bai": "content/lesson-samples/l10-lam-quen-voi-vat-li/theory.html"}
tn = [
    {**BASE, "id": "tn-l10-lam-quen-01",
     "ten": "Giọt mực trong nước nóng và nước lạnh: vĩ mô nhìn thấy, vi mô giải thích",
     "loai": "thi_nghiem", "muc_do": "co_ban",
     "kien_thuc": ["lamquen.doi_tuong", "lamquen.cap_do", "lamquen.chuyen_dong_nhiet"],
     "muc_tieu": "Nhìn hiện tượng vĩ mô (mực loang) và giải thích bằng chuyển động của phân tử (vi mô); thấy nhiệt độ càng cao thì loang càng nhanh.",
     "dung_cu": [{"ten": "Cốc thuỷ tinh trong", "so_luong": 2}, {"ten": "Mực màu (hoặc thuốc nhuộm thực phẩm)", "so_luong": 1},
                 {"ten": "Nước lạnh và nước nóng khoảng 60 °C", "so_luong": 1}],
     "cac_buoc": {"lam": ["Rót nước lạnh vào cốc 1, nước nóng khoảng 60 °C vào cốc 2 (cùng lượng).", "Nhỏ một giọt mực vào mỗi cốc, không khuấy, để yên."],
                  "quan_sat": ["Mực trong cốc nóng loang đều nhanh hơn hẳn cốc lạnh."],
                  "rut_ra": ["Cái thấy được (mực loang) là hiện tượng vĩ mô.", "Nguyên nhân vi mô: phân tử nước chuyển động nhiệt, nước càng nóng chuyển động càng nhanh."]},
     "tham_so": [{"ky_hieu": "T", "ten": "Nhiệt độ nước", "don_vi": "°C", "kieu": "dieu_chinh", "min": 10, "max": 80, "mac_dinh": 60, "buoc": 5},
                 {"ky_hieu": "t_loang", "ten": "Thời gian mực loang đều", "don_vi": "s", "kieu": "tinh_ra"}],
     "mo_hinh": {"phuong_trinh": ["tốc độ loang tăng khi nhiệt độ T tăng (chuyển động nhiệt của phân tử mạnh hơn)"],
                 "gia_thiet": ["không khuấy, không có đối lưu mạnh", "chỉ xét ảnh hưởng của nhiệt độ"]},
     "so_lieu_mau": {"cot": ["Cốc", "Mực loang đều"],
                     "hang": [["nước lạnh", "chậm"], ["nước nóng ~60 °C", "nhanh hơn rõ rệt"]],
                     "ghi_chu": "Thí nghiệm định tính, không có số đo; ở giai đoạn mô phỏng sẽ gán thời gian theo mô hình khuếch tán."},
     "ket_qua_ky_vong": "Cốc nước nóng loang đều trước cốc nước lạnh.",
     "hien_tuong_hay_sai": ["Cho rằng mực loang vì mực nặng hơn nên chìm xuống (bỏ qua chuyển động phân tử).", "Nghĩ vật lí chỉ nghiên cứu cái nhìn thấy được."],
     "sai_so_thuong_gap": "Nước nóng tạo đối lưu làm trộn mực; khó xác định lúc 'loang đều'.",
     "an_toan": "Nước nóng 60 °C: rót cẩn thận, tránh bỏng.",
     "goi_y_mo_phong": {"loai": "2d_dong_hoc",
                        "y_tuong": "Hai cốc nhìn từ bên, hạt mực là các chấm chuyển động ngẫu nhiên; nút phóng to xuống mức phân tử.",
                        "diem_nhan": "Thanh trượt nhiệt độ làm vận tốc phân tử tăng, thấy mực loang nhanh hơn ở mức vĩ mô."}},
    {**BASE, "id": "tn-l10-lam-quen-02",
     "ten": "Sách và tờ giấy rơi: cả 5 bước nghiên cứu trên một ví dụ",
     "loai": "thi_nghiem", "muc_do": "trung_binh",
     "kien_thuc": ["lamquen.quy_trinh_5_buoc", "lamquen.thuc_nghiem", "lamquen.sai_so_phep_do"],
     "muc_tieu": "Đi hết quy trình: quan sát sách rơi nhanh hơn giấy, đặt giả thuyết 'không khí cản', kiểm tra bằng giấy đặt trên sách và giấy vo tròn, rút ra kết luận, và đọc bảng số liệu có sai số.",
     "dung_cu": [{"ten": "Quyển sách", "so_luong": 1}, {"ten": "Tờ giấy A4", "so_luong": 1},
                 {"ten": "Điện thoại quay video 60 hình/giây", "so_luong": 1}, {"ten": "Thước dây (đánh dấu độ cao 2 m)", "so_luong": 1}],
     "cac_buoc": {"lam": ["Thả cùng lúc sách và tờ giấy phẳng từ độ cao 2 m.", "Đặt tờ giấy lên mặt sách rồi thả.",
                          "Vo tròn tờ giấy rồi thả cùng sách; quay video, đếm khung hình từ lúc buông tới lúc chạm sàn; sách và giấy vo thả mỗi kiểu 3 lần, giấy phẳng và giấy đặt trên sách chỉ quan sát định tính."],
                  "quan_sat": ["Giấy phẳng rơi chậm hơn nhiều; giấy đặt trên sách rơi cùng sách.",
                               "Sách: " + ", ".join(map(str, FR_SACH)) + " khung hình; giấy vo tròn: " + ", ".join(map(str, FR_VO)) + " khung hình."],
                  "rut_ra": ["Nặng hơn không làm rơi nhanh hơn: giả thuyết 'vật nặng rơi nhanh hơn' bị bác bỏ.",
                             "Giấy phẳng chậm vì không khí cản: giả thuyết của Lan được ủng hộ; chênh " + vp(CHENH, 1) + " khung hình giữa sách và giấy vo lớn hơn sai số ±1 khung hình."]},
     "tham_so": [{"ky_hieu": "h", "ten": "Độ cao thả", "don_vi": "m", "kieu": "dieu_chinh", "min": 1, "max": 3, "mac_dinh": H, "buoc": 0.5},
                 {"ky_hieu": "k_can", "ten": "Hệ số cản làm chậm (giấy vo tròn)", "don_vi": "", "kieu": "dieu_chinh", "min": 1.0, "max": 1.5, "mac_dinh": K_VO, "buoc": 0.01},
                 {"ky_hieu": "g", "ten": "Gia tốc rơi tự do", "don_vi": "m/s²", "kieu": "co_dinh", "gia_tri": G},
                 {"ky_hieu": "fps", "ten": "Số hình mỗi giây của video", "don_vi": "hình/s", "kieu": "co_dinh", "gia_tri": FPS},
                 {"ky_hieu": "n_khung", "ten": "Số khung hình đếm được", "don_vi": "", "kieu": "do_duoc", "sai_so_do": 1}],
     "mo_hinh": {"phuong_trinh": ["t_sách = sqrt(2h/g)", "t_giấy_vo = k_can · t_sách", "n = floor(t·fps + pha), pha ∈ {0; 0,4; 0,8} (thời điểm buông lệch so với khung hình)", "g_tính = 2h/t_tb²"],
                 "gia_thiet": ["sách rơi tự do, bỏ cản không khí", "k_can = 1,07 là GIẢ ĐỊNH minh hoạ cho giấy vo tròn", "giấy phẳng: không lập mô hình số, chỉ định tính"]},
     "so_lieu_mau": {"cot": ["Vật", "Lần 1", "Lần 2", "Lần 3", "t_tb (s)"],
                     "hang": [["Sách"] + FR_SACH + [round(TS, 3)], ["Giấy vo tròn"] + FR_VO + [round(TV, 3)]],
                     "ghi_chu": f"Số liệu minh hoạ tính từ mô hình: t_sách = {T_SACH:.4f} s; sách trung bình {MEAN_S:.2f} khung = {TS:.4f} s → g = {G_TINH:.2f} m/s²; giấy vo {MEAN_V:.0f} khung = {TV:.4f} s. Chênh {CHENH:.2f} khung > sai số ±1."},
     "ket_qua_ky_vong": "Sách ≈ 0,64 s, giấy vo ≈ 0,68 s; g tính từ sách ≈ 9,8 m/s²; giấy phẳng chậm rõ rệt, giấy đặt trên sách rơi cùng sách.",
     "hien_tuong_hay_sai": ["Kết luận 'vật nặng rơi nhanh hơn' chỉ từ một lần quan sát.", "Coi lần đo lệch 1 khung hình là đo hỏng.", "Coi giả thuyết bị bác bỏ là thí nghiệm thất bại."],
     "sai_so_thuong_gap": "Thời điểm buông không khớp khung hình (±1 khung = ±0,017 s); khó chọn khung chạm sàn; giấy lật khi rơi.",
     "goi_y_mo_phong": {"loai": "2d_dong_hoc+bang_so_lieu",
                        "y_tuong": "Ba làn thả cạnh nhau, đồng hồ khung hình chạy; thanh trượt độ cao và hệ số cản; bảng tự điền số khung hình ba lần với pha buông ngẫu nhiên.",
                        "diem_nhan": "Tắt không khí (k_can = 1) thì giấy và sách chạm sàn cùng lúc, thấy rõ giả thuyết 'không khí cản'."}},
    {**BASE, "id": "tn-l10-lam-quen-03",
     "ten": "Robot hút bụi đi hình vuông: dự đoán lí thuyết 30 s, đo thật 33 s",
     "loai": "vi_du", "muc_do": "trung_binh",
     "kien_thuc": ["lamquen.ly_thuyet", "lamquen.thuc_nghiem", "lamquen.ly_thuyet_thuc_nghiem_bo_sung"],
     "muc_tieu": "Thấy lí thuyết và thực nghiệm bổ sung nhau: dự đoán t = L/v, đo thật lệch vì bỏ sót giảm tốc khi rẽ ở góc; chênh lệch chỉ ra chỗ cần sửa mô hình.",
     "dung_cu": [{"ten": "Không cần (ví dụ phân tích; ngoài đời dùng robot hút bụi và đồng hồ bấm giây)", "so_luong": 0}],
     "cac_buoc": {"lam": ["Cho robot hút bụi đi dọc bốn cạnh một ô vuông cạnh 1,5 m (chu vi 6 m) với tốc độ 0,2 m/s.", "Tính lí thuyết: t = 6/0,2 = 30 s."],
                  "quan_sat": ["Đồng hồ bấm giây báo 33 s (số liệu minh hoạ)."],
                  "rut_ra": ["Dự đoán 30 s lệch số đo 33 s là 3 s (10 %).", "Nguyên nhân: mô hình chỉ tính chạy đều, bỏ sót giảm tốc khi rẽ ở 4 góc (mỗi góc khoảng 0,75 s).", "Sửa mô hình rồi đo lại: lí thuyết giải thích thực nghiệm, thực nghiệm kiểm chứng lí thuyết."]},
     "tham_so": [{"ky_hieu": "L", "ten": "Chiều dài đường đi của robot", "don_vi": "m", "kieu": "dieu_chinh", "min": 2, "max": 12, "mac_dinh": L_CNC, "buoc": 1},
                 {"ky_hieu": "v", "ten": "Tốc độ của robot", "don_vi": "m/s", "kieu": "dieu_chinh", "min": 0.1, "max": 0.5, "mac_dinh": V_CNC, "buoc": 0.05},
                 {"ky_hieu": "n_goc", "ten": "Số góc của đường đi", "don_vi": "", "kieu": "dieu_chinh", "min": 0, "max": 8, "mac_dinh": N_GOC, "buoc": 1},
                 {"ky_hieu": "t_goc", "ten": "Thời gian mất thêm mỗi góc do rẽ", "don_vi": "s", "kieu": "co_dinh", "gia_tri": T_GOC},
                 {"ky_hieu": "t", "ten": "Thời gian chạy", "don_vi": "s", "kieu": "tinh_ra"}],
     "mo_hinh": {"phuong_trinh": ["t_lí_thuyết = L/v", "t_đo = t_lí_thuyết + n_goc·t_goc"],
                 "gia_thiet": ["t_goc = 0,75 s là GIẢ ĐỊNH minh hoạ", "bỏ qua thời gian tăng tốc ban đầu và dừng cuối"]},
     "so_lieu_mau": {"cot": ["L (m)", "v (m/s)", "Số góc", "t lí thuyết (s)", "t đo (s)"],
                     "hang": [[L_CNC, V_CNC, N_GOC, T_LT, T_DO], [9, 0.25, N_GOC, T2, T2 + N_GOC * T_GOC]],
                     "ghi_chu": "Số liệu minh hoạ tính từ mô hình; hàng 2 là thử thách ⭐⭐ (đo thật 39 s)."},
     "ket_qua_ky_vong": "Lí thuyết 30 s, đo 33 s, lệch 10 %; nguyên nhân: giảm tốc khi rẽ ở 4 góc.",
     "hien_tuong_hay_sai": ["Bỏ kết quả đo vì lí thuyết 'đã tính chắc chắn'.", "Bỏ cả phép tính vì lệch 10 %."],
     "sai_so_thuong_gap": "Đồng hồ máy làm tròn giây; tốc độ thực khác tốc độ đặt.",
     "goi_y_mo_phong": {"loai": "2d_dong_hoc+bang_so_lieu",
                        "y_tuong": "Robot chạy theo hình vuông; hai đồng hồ: dự đoán lí thuyết và thời gian đo; thanh trượt số góc và t_goc.",
                        "diem_nhan": "Cho t_goc = 0 thì hai đồng hồ trùng nhau, thấy yếu tố bị bỏ sót."}},
]
for d in tn:
    (ROOT / "content/thi-nghiem" / f"{d['id']}.json").write_text(json.dumps(d, ensure_ascii=False, indent=1) + "\n", encoding="utf8")
print(f"ok theory.html {len(h)} ký tự · 3 hình · {phut} phút · 3 file thí nghiệm · g_tính = {G_TINH:.3f} · chênh = {CHENH:.2f}")
