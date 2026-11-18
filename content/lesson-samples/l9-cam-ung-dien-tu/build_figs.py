"""Bài 14. Cảm ứng điện từ. Nguyên tắc tạo ra dòng điện xoay chiều (KHTN 9, lesson_id 92).
Sinh 4 hình SVG + bảng số liệu thí nghiệm + 3 file content/thi-nghiem/tn-l9-camung-0N.json,
thay mốc <!--FIGn--> / __...__ trong theory.src.html -> theory.html.
Đường sức Hình 3 tính bằng mô hình hai cực từ (vết theo trường 1/r^2), số đường xuyên qua cuộn dây đếm bằng máy.
Chạy: cd <thư mục bài> && python3 build_figs.py
"""
import json, math, pathlib
from svg_lib import *

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[2]
PHUT = 16          # số phút đọc: lấy từ lint_do_dai.py, làm tròn lên


def vn(x, nd=1):
    return f"{x:.{nd}f}".replace(".", "{,}")
def line(x1, y1, x2, y2, c="currentColor", w=2, dash="", op=1):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{c}" stroke-width="{w}"{d} opacity="{op}"/>'
def T(x, y, s, c="currentColor", size=15, anchor="start", weight="700"):
    return text(x, y, s, c, size, anchor, weight)
def coil(x0, x1, cy, ry, n, rx=8, c="currentColor", w=2.2):
    """Cuộn dây nhìn ngang: n vòng (ellipse), nửa sau mờ, nửa trước đậm."""
    o = ""
    for k in range(n):
        cx = x0 + (x1 - x0) * k / (n - 1)
        o += pts_path(arc_pts(cx, cy, rx, ry, 90, 270), c, w * .7, "") .replace('stroke-width', 'opacity=".45" stroke-width')
        o += pts_path(arc_pts(cx, cy, rx, ry, -90, 90), c, w)
    return o
def galvo(cx, cy, r=30):
    """Điện kế: vòng tròn, thang chia hình cung, số 0 ở giữa, kim đứng ở 0."""
    o = f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="rgba(56,189,248,.10)" stroke="currentColor" stroke-width="2.2"/>'
    pc = (cx, cy + 6)
    R = r - 10
    o += pts_path(arc_pts(pc[0], pc[1], R, R, 215, 325), "currentColor", 1.6)
    for a in (215, 242.5, 270, 297.5, 325):
        x1, y1 = ell_pt(pc[0], pc[1], R, R, a)
        x2, y2 = ell_pt(pc[0], pc[1], R + (6 if a == 270 else 4), R + (6 if a == 270 else 4), a)
        o += line(x1, y1, x2, y2, "currentColor", 2 if a == 270 else 1.4)
    o += line(pc[0], pc[1], pc[0], pc[1] - R + 2, RED, 2.4)
    o += f'<circle cx="{pc[0]}" cy="{pc[1]}" r="3" fill="currentColor"/>'
    o += T(cx, cy + r - 6, "G", "currentColor", 13, "middle", "800")
    return o


# ---------- Hình 1: đinamô xe đạp (cảnh mở bài, không nói cơ chế)
b = ""
WX, WY, WR = 120, 160, 78
b += f'<circle cx="{WX}" cy="{WY}" r="{WR}" fill="none" stroke="currentColor" stroke-width="7"/>'
b += f'<circle cx="{WX}" cy="{WY}" r="{WR - 9}" fill="none" stroke="currentColor" stroke-width="1.6" opacity=".7"/>'
for k in range(12):
    a = math.radians(15 + 30 * k)
    b += line(WX, WY, WX + (WR - 10) * math.cos(a), WY + (WR - 10) * math.sin(a), "currentColor", 1.2, "", .6)
b += f'<circle cx="{WX}" cy="{WY}" r="7" fill="currentColor"/>'
# càng xe: từ trục bánh lên ghi đông
b += line(WX, WY, 188, 28, "currentColor", 5)
# đinamô: tì vào lốp ở góc -50°
ang = -50
ux, uy = math.cos(math.radians(ang)), math.sin(math.radians(ang))
cx_, cy_ = WX + (WR + 4) * ux, WY + (WR + 4) * uy          # điểm tì trên lốp
g = (f'<g transform="translate({cx_:.1f},{cy_:.1f}) rotate({ang})">'
     '<rect x="0" y="-6" width="12" height="12" rx="3" fill="currentColor"/>'
     '<rect x="12" y="-13" width="50" height="26" rx="8" fill="rgba(251,146,60,.25)" stroke="currentColor" stroke-width="2.2"/>'
     '</g>')
b += g
top = (cx_ + 62 * ux, cy_ + 62 * uy)
# dây từ đầu đinamô tới đèn
b += f'<path d="M{top[0]:.1f},{top[1]:.1f} C{top[0] + 30:.1f},{top[1] - 30:.1f} 250,40 286,62" fill="none" stroke="currentColor" stroke-width="1.8"/>'
# đèn xe
b += '<path d="M286,48 h26 l18,-12 v52 l-18,-12 h-26 z" fill="rgba(251,146,60,.18)" stroke="currentColor" stroke-width="2.2" stroke-linejoin="round"/>'
for dy in (-22, 0, 22):
    b += line(340, 62 + dy * .6, 392, 62 + dy * 1.4, ORG, 2.4)
# mũi tên quay của bánh xe (cùng chiều kim đồng hồ khi xe chạy sang phải)
P = arc_pts(WX, WY, WR + 18, WR + 18, 200, 250)
b += pts_path(P, GRN, 2.6) + chev_on(P, len(P) - 2, GRN, 2.6)
b += T(196, 112, "Đinamô", "currentColor", 16)
b += T(290, 120, "Đèn xe", "currentColor", 16)
b += T(12, 26, "Bánh xe quay", GRN, 15)
fig1 = wrap("0 0 420 250", "Bánh xe đạp, đinamô hình trụ tì vào lốp, dây nối từ đinamô tới đèn xe phía trước", b,
            "Hình 1. Đèn xe đạp chạy bằng đinamô.<br>Núm đinamô tì vào lốp, quay theo bánh xe.")

# ---------- Hình 2: bố trí Thí nghiệm 1
b = ""
MCX, MCY = 92, 112
b += line(MCX, 58, MCX, 168, "currentColor", 1.6, "5 4", .7)          # trục quay của giá
P = arc_pts(MCX, 62, 26, 8, 160, 380)
b += pts_path(P, GRN, 2.2) + chev_on(P, len(P) - 2, GRN, 2.2, 10)
b += bar_magnet(MCX, MCY, 104, 32, n_left=False)
# mũi tên hai chiều: lại gần / ra xa
b += line(52, 160, 136, 160, BLUE, 2.4) + chevron(136, 160, 1, 0, BLUE, 2.4, 11) + chevron(52, 160, -1, 0, BLUE, 2.4, 11)
b += T(94, 184, "lại gần · ra xa", BLUE, 14, "middle")
b += T(136, 64, "quay", GRN, 14)
b += T(10, 28, "(1) Nam châm", "currentColor", 15)
# cuộn dây
X0, X1, RY = 214, 314, 38
b += coil(X0, X1, MCY, RY, 8)
b += line(X0, MCY - RY, X1, MCY - RY, "currentColor", 1.2, "", .5) + line(X0, MCY + RY, X1, MCY + RY, "currentColor", 1.2, "", .5)
b += T(214, 56, "(2) Cuộn dây", "currentColor", 15)
# dây nối + điện kế
GX, GY = 264, 222
b += f'<path d="M{X0},{MCY + RY} V{GY} H{GX - 30}" fill="none" stroke="currentColor" stroke-width="2"/>'
b += f'<path d="M{X1},{MCY + RY} V{GY} H{GX + 30}" fill="none" stroke="currentColor" stroke-width="2"/>'
b += galvo(GX, GY, 30)
b += T(322, 200, "(4) Dây nối", "currentColor", 14)
b += T(322, 248, "(3) Điện kế", "currentColor", 14)
fig2 = wrap("0 0 420 262", "Nam châm thẳng trên giá có trục quay đặt trước cuộn dây, hai đầu cuộn dây nối với điện kế có số 0 ở giữa", b,
            "Hình 2. Bố trí Thí nghiệm 1.<br>Điện kế có số 0 ở giữa: kim lệch trái hay phải cho biết chiều dòng điện.")


# ---------- Hình 3: đường sức xuyên qua cuộn dây ở xa và ở gần (mô hình hai cực từ)
def trace(qs, start, box, ds=1.2, nmax=4000):
    pts = [start]
    x, y = start
    for _ in range(nmax):
        ex = ey = 0.0
        for (qx, qy, q) in qs:
            dx, dy = x - qx, y - qy
            r3 = (dx * dx + dy * dy) ** 1.5 or 1e-9
            ex += q * dx / r3; ey += q * dy / r3
        n = math.hypot(ex, ey) or 1e-9
        # bước giữa (RK2)
        xm, ym = x + ex / n * ds / 2, y + ey / n * ds / 2
        ex = ey = 0.0
        for (qx, qy, q) in qs:
            dx, dy = xm - qx, ym - qy
            r3 = (dx * dx + dy * dy) ** 1.5 or 1e-9
            ex += q * dx / r3; ey += q * dy / r3
        n = math.hypot(ex, ey) or 1e-9
        x, y = x + ex / n * ds, y + ey / n * ds
        pts.append((x, y))
        if any(q < 0 and math.hypot(x - qx, y - qy) < 4 for (qx, qy, q) in qs):
            break
        if not (box[0] <= x <= box[2] and box[1] <= y <= box[3]):
            break
    return pts

def crosses(pts, xl, cy, a):
    """Đường sức có đi qua mặt phẳng x = xl theo chiều +x trong khoảng |y - cy| < a?"""
    for (x1, y1), (x2, y2) in zip(pts, pts[1:]):
        if x1 < xl <= x2:
            yy = y1 + (y2 - y1) * (xl - x1) / (x2 - x1)
            if abs(yy - cy) < a:
                return True
    return False

def panel(y0, cy, xl, tag, prefix):
    o = ""
    MXc, ML = 78, 92
    xN, xS = MXc + ML / 2 - 6, MXc - ML / 2 + 6
    qs = [(xN, cy, 1.0), (xS, cy, -1.0)]
    box = (0, y0 + 26, 420, y0 + 134)
    A = 30                                  # bán kính cuộn dây (px)
    n_qua = 0
    for th in range(-150, 151, 15):
        s = (xN + 3 * math.cos(math.radians(th)), cy + 3 * math.sin(math.radians(th)))
        P = trace(qs, s, box)
        hit = crosses(P, xl, cy, A)
        n_qua += hit
        col = BLUE if hit else "currentColor"
        op = "1" if hit else ".45"
        d = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in P[::3])
        o += f'<path d="{d}" fill="none" stroke="{col}" stroke-width="{2 if hit else 1.5}" stroke-dasharray="6 4" opacity="{op}"/>'
        # đầu V ở điểm cách cực N khoảng 70 px theo đường (ngoài thân nam châm)
        L = 0
        for i in range(1, len(P) - 1):
            L += math.hypot(P[i][0] - P[i - 1][0], P[i][1] - P[i - 1][1])
            if L > 62 and not (MXc - ML / 2 - 4 < P[i][0] < MXc + ML / 2 + 4 and abs(P[i][1] - cy) < 18):
                if box[0] + 6 < P[i][0] < box[2] - 6 and box[1] + 6 < P[i][1] < box[3] - 6:
                    o += f'<g opacity="{op}">' + chevron(P[i][0], P[i][1], P[i + 1][0] - P[i][0], P[i + 1][1] - P[i][1], col, 1.8, 9) + "</g>"
                break
    o += bar_magnet(MXc, cy, ML, 26, d=(8, -6), fs=15, n_left=False)
    # cuộn dây (một vòng, nhìn nghiêng)
    o += pts_path(arc_pts(xl, cy, 8, A, 90, 270), ORG, 2.4)
    o += pts_path(arc_pts(xl, cy, 8, A, -90, 90), ORG, 3)
    o += T(10, y0 + 18, tag, "currentColor", 15)
    return o, n_qua

pa, n_xa = panel(0, 80, 330, "a) Cuộn dây ở xa", "a")
pb, n_gan = panel(146, 226, 160, "b) Cuộn dây ở gần", "b")
assert n_gan > n_xa >= 1, (n_xa, n_gan)
b = pa + pb + line(0, 140, 420, 140, "currentColor", 1, "3 4", .4)
b += T(410, 18, f"{n_xa} đường xuyên qua", BLUE, 15, "end")
b += T(410, 164, f"{n_gan} đường xuyên qua", BLUE, 15, "end")
fig3 = wrap("0 0 420 282", f"Cùng một nam châm thẳng, đường sức nét đứt; vòng dây ở xa có {n_xa} đường sức xuyên qua, ở gần có {n_gan} đường", b,
            f"Hình 3. Đường sức xuyên qua cuộn dây (tô xanh).<br>Ở xa: {n_xa} đường. Ở gần: {n_gan} đường.")


# ---------- Hình 4: nam châm quay trước cuộn dây, hai LED song song ngược chiều (nhìn từ trên)
def led(x, y, up, col):
    """Kí hiệu LED trên dây dọc tại (x, y): tam giác chỉ chiều dòng đi qua được (up=True: từ dưới lên)."""
    s = -1 if up else 1
    o = (f'<polygon points="{x - 12},{y - 9 * s} {x + 12},{y - 9 * s} {x},{y + 9 * s}" fill="{col}" fill-opacity=".35" '
         f'stroke="currentColor" stroke-width="2" stroke-linejoin="round"/>')
    o += line(x - 12, y + 9 * s, x + 12, y + 9 * s, "currentColor", 2.4)
    for k in (0, 1):
        ax, ay = x + 16, y - 6 + 10 * k
        o += line(ax, ay, ax + 10, ay - 7, col, 2) + chevron(ax + 10, ay - 7, 10, -7, col, 2, 6)
    return o

b = ""
CX, CY, ROT = 92, 128, -35
b += f'<circle cx="{CX}" cy="{CY}" r="66" fill="none" stroke="currentColor" stroke-width="1" stroke-dasharray="3 5" opacity=".5"/>'
b += (f'<g transform="rotate({ROT} {CX} {CY})">'
      f'<rect x="{CX - 54}" y="{CY - 14}" width="54" height="28" fill="{UM_S[0]}" stroke="{UM_EDGE}" stroke-width="2"/>'
      f'<rect x="{CX}" y="{CY - 14}" width="54" height="28" fill="{UM_N[0]}" stroke="{UM_EDGE}" stroke-width="2"/>'
      + text(CX - 27, CY + 6, "S", "#fff", 16, "middle", "800") + text(CX + 27, CY + 6, "N", "#fff", 16, "middle", "800") + "</g>")
b += f'<circle cx="{CX}" cy="{CY}" r="4" fill="#fff" stroke="{UM_EDGE}" stroke-width="2"/>'
P = arc_pts(CX, CY, 78, 78, 200, 300)
b += pts_path(P, GRN, 2.6) + chev_on(P, len(P) - 2, GRN, 2.6)
b += T(10, 30, "Nam châm quay", GRN, 15)
b += T(10, 238, "trục quay ở tâm", "currentColor", 13, "start", "600")
# cuộn dây
X0, X1, RY = 186, 262, 34
b += coil(X0, X1, CY, RY, 6, 7)
b += T(222, 196, "Cuộn dây", "currentColor", 15, "middle")
# dây nối và hai LED
XR, XG, YT, YB = 324, 384, 48, 214
b += f'<path d="M{X0},{CY - RY} V{YT} H{XG} V{CY - 12}" fill="none" stroke="currentColor" stroke-width="2"/>'
b += f'<path d="M{X1},{CY + RY} V{YB} H{XG} V{CY + 12}" fill="none" stroke="currentColor" stroke-width="2"/>'
b += line(XR, YT, XR, CY - 12) + line(XR, CY + 12, XR, YB)
b += f'<circle cx="{XR}" cy="{YT}" r="3" fill="currentColor"/><circle cx="{XR}" cy="{YB}" r="3" fill="currentColor"/>'
b += led(XR, CY, False, RED) + led(XG, CY, True, GRN)
b += T(XR, 236, "LED đỏ", RED, 14, "middle")
b += T(XG - 8, 256, "LED xanh", GRN, 14, "middle")
fig4 = wrap("0 0 420 264", "Nhìn từ trên: nam châm thẳng quay quanh trục ở tâm, đặt trước cuộn dây; hai đầu cuộn dây nối với hai đèn LED đỏ và xanh mắc song song, ngược chiều nhau", b,
            "Hình 4. Thí nghiệm 3, nhìn từ trên xuống.<br>Hai LED mắc song song, ngược chiều nhau.<br>Mỗi LED chỉ cho dòng điện đi qua theo chiều mũi tam giác.")


# ---------- Số liệu đo thêm của Thí nghiệm 1: đưa cực N vào cuộn dây trong t giây, đọc số chỉ lớn nhất i (mA)
# Mô hình: i_that = K / t (đưa nhanh gấp đôi, số đường sức đổi nhanh gấp đôi). Số đọc = i_that trừ phần kim không kịp lệch hết
# (quán tính kim, rõ ở lần nhanh nhất) + lệch ngẫu nhiên do tay đưa không đều.
K = 1.0
T_DUA = [2.0, 1.0, 0.5]
DOC = {2.0: [0.6, 0.5, 0.4], 1.0: [1.1, 0.9, 1.0], 0.5: [1.9, 1.7, 1.8]}
rows = []
for t in T_DUA:
    tb = sum(DOC[t]) / 3
    rows.append((t, DOC[t], tb, K / t))
assert abs(rows[0][2] - 0.5) < 1e-9 and abs(rows[1][2] - 1.0) < 1e-9 and abs(rows[2][2] - 1.8) < 1e-9
assert rows[2][2] < rows[2][3]           # lần nhanh nhất: số đọc nhỏ hơn mô hình (kim có quán tính)
bang = "\n".join(f'<tr><td>${vn(t)}\\ \\text{{s}}$</td><td>${"; ".join(vn(v) for v in d)}$</td><td>${vn(tb)}$</td></tr>'
                 for t, d, tb, _ in rows)

# ---------- Dựng theory.html
h = (HERE / "theory.src.html").read_text(encoding="utf8")
for k, v in (("__BANG_TN1__", bang), ("__PHUT__", str(PHUT))):
    assert k in h, k
    h = h.replace(k, v)
for n, fg in enumerate((fig1, fig2, fig3, fig4), 1):
    assert f"<!--FIG{n}-->" in h, n
    h = h.replace(f"<!--FIG{n}-->", fg)
assert "__" not in h.replace("___", "")
(HERE / "theory.html").write_text(h, encoding="utf8")

# ---------- Kho thí nghiệm
BAI = "Bài 14. Cảm ứng điện từ. Nguyên tắc tạo ra dòng điện xoay chiều"
SRC = "content/lesson-samples/l9-cam-ung-dien-tu/theory.html"
base = {"mon": "vat-ly", "lop": 9, "bai": BAI, "lesson_id": 92, "nguon_trong_bai": SRC}
tn = []
tn.append({**base,
  "id": "tn-l9-camung-01", "ten": "Thí nghiệm Faraday: nam châm thẳng và cuộn dây nối điện kế", "loai": "thi_nghiem", "muc_do": "co_ban",
  "kien_thuc": ["camung.hien_tuong", "camung.dieu_kien_bien_thien", "camung.doi_chieu"],
  "muc_tieu": "Thấy nam châm đứng yên không tạo ra dòng điện; chỉ khi nam châm chuyển động (lại gần, ra xa, quay) so với cuộn dây kín mới có dòng điện cảm ứng; lại gần và ra xa cho hai chiều ngược nhau.",
  "gia_thuyet": ["Cứ có nam châm đặt cạnh cuộn dây kín là có dòng điện trong cuộn dây."],
  "du_doan_neu_dung": ["Nam châm đứng yên sát cuộn dây, kim điện kế vẫn lệch."],
  "khong_chung_minh": ["Chưa cho biết cái gì thay đổi mới là nguyên nhân (số đường sức qua cuộn dây).",
                       "Bảng tốc độ chỉ là số liệu minh hoạ; chưa đo được dòng cảm ứng chính xác bao nhiêu ampe."],
  "dung_cu": [{"ten": "Nam châm thẳng đặt trên giá có trục quay thẳng đứng qua giữa nam châm", "so_luong": 1},
              {"ten": "Cuộn dây dẫn (vài trăm vòng)", "so_luong": 1},
              {"ten": "Điện kế có số 0 ở giữa thang đo", "so_luong": 1},
              {"ten": "Dây nối", "so_luong": 2}],
  "cac_buoc": {"lam": ["Nối hai đầu cuộn dây với điện kế (không có pin).",
                       "Giữ yên nam châm trước cuộn dây, nhìn kim.",
                       "Đưa nam châm lại gần cuộn dây, rồi kéo ra xa.",
                       "Quay nam châm quanh trục của giá.",
                       "Đưa cực N vào cuộn dây trong 2 s, 1 s, 0,5 s; mỗi cách 3 lần, ghi số chỉ lớn nhất của điện kế."],
               "quan_sat": ["Nam châm đứng yên: kim chỉ số 0.", "Lại gần: kim lệch một phía; ra xa: kim lệch phía ngược lại.",
                            "Quay: kim lệch qua lại liên tục.", "Đưa càng nhanh, kim lệch càng nhiều (bảng)."],
               "rut_ra": ["Giả thuyết bị bác bỏ: nam châm đứng yên không tạo ra dòng điện.",
                          "Nam châm chuyển động so với cuộn dây kín thì trong cuộn dây có dòng điện cảm ứng.",
                          "Lại gần và ra xa cho dòng cảm ứng ngược chiều nhau."]},
  "tham_so": [{"ky_hieu": "t", "ten": "Thời gian đưa cực N vào cuộn dây", "don_vi": "s", "kieu": "dieu_chinh", "min": 0.25, "max": 3, "mac_dinh": 1, "buoc": 0.25},
              {"ky_hieu": "K", "ten": "Hệ số của bộ dụng cụ (i = K/t)", "don_vi": "mA·s", "kieu": "co_dinh", "gia_tri": K},
              {"ky_hieu": "i", "ten": "Số chỉ lớn nhất của điện kế", "don_vi": "mA", "kieu": "do_duoc", "sai_so_do": 0.1}],
  "mo_hinh": {"phuong_trinh": ["i = K/t (số đường sức đổi càng nhanh, dòng càng lớn)", "nam châm đứng yên: i = 0",
                               "i_doc nhỏ hơn i một chút khi t nhỏ (kim có quán tính)"],
              "gia_thiet": ["coi rằng gần đó không có nam châm hay dòng điện nào khác", "bỏ qua từ trường Trái Đất",
                            "đưa nam châm gần như đều tay"]},
  "so_lieu_mau": {"cot": ["t (s)", "Lần 1 (mA)", "Lần 2 (mA)", "Lần 3 (mA)", "Trung bình (mA)"],
                  "hang": [[t, *d, round(tb, 2)] for t, d, tb, _ in rows],
                  "ghi_chu": "Số liệu minh hoạ từ mô hình i = 1,0/t, có lệch tay và quán tính kim; chưa phải số đo thật."},
  "ket_qua_ky_vong": "Đứng yên: 0. Lại gần và ra xa: kim lệch hai phía ngược nhau. Đưa nhanh gấp đôi thì số chỉ gần gấp đôi.",
  "hien_tuong_hay_sai": ["Nghĩ nam châm mạnh để yên trong cuộn dây vẫn có dòng điện.",
                         "Nghĩ lại gần và ra xa cho dòng cùng chiều.",
                         "Quên rằng cuộn dây phải nối kín với điện kế."],
  "sai_so_thuong_gap": "Lần đưa nhanh nhất, kim có quán tính nên số chỉ lớn nhất đọc được nhỏ hơn giá trị thật; tay đưa không đều làm ba lần lệch nhau, lấy trung bình để giảm.",
  "an_toan": "Không đập nam châm vào cuộn dây; giữ nam châm xa điện thoại, thẻ từ.",
  "goi_y_mo_phong": {"loai": "2d_dong_hoc+bang_so_lieu", "y_tuong": "Kéo nam châm bằng chuột trước cuộn dây; kim điện kế lệch theo tốc độ và chiều chuyển động, đứng yên thì về 0.",
                     "diem_nhan": "Để yên nam châm ngay trong lòng cuộn dây: kim về 0."}})
tn.append({**base,
  "id": "tn-l9-camung-02", "ten": "Nam châm điện: đóng, giữ đóng, ngắt công tắc", "loai": "thi_nghiem", "muc_do": "co_ban",
  "kien_thuc": ["camung.hien_tuong", "camung.dieu_kien_bien_thien"],
  "muc_tieu": "Thấy nam châm điện cũng tạo được dòng cảm ứng, nhưng chỉ trong lúc đóng hoặc ngắt công tắc, khi dòng điện trong cuộn A đang thay đổi.",
  "dung_cu": [{"ten": "Cuộn dây A nối với bộ pin 4 × 1,5 V qua công tắc (nam châm điện)", "so_luong": 1},
              {"ten": "Cuộn dây B nối với điện kế có số 0 ở giữa", "so_luong": 1},
              {"ten": "Công tắc và dây nối", "so_luong": 1}],
  "cac_buoc": {"lam": ["Đặt cuộn A sát cuộn B, công tắc đang mở.", "Đóng công tắc, rồi giữ đóng một lúc.", "Ngắt công tắc."],
               "quan_sat": ["Trong lúc đóng: kim lệch một phía rồi về 0.", "Giữ đóng: kim đứng ở số 0.",
                            "Trong lúc ngắt: kim lệch phía ngược lại rồi về 0."],
               "rut_ra": ["Chỉ khi dòng điện trong cuộn A đang thay đổi, từ trường qua cuộn B thay đổi và cuộn B có dòng cảm ứng.",
                          "Nam châm điện đang có dòng không đổi, dù mạnh, không tạo ra dòng cảm ứng."]},
  "tham_so": [{"ky_hieu": "U", "ten": "Hiệu điện thế bộ pin", "don_vi": "V", "kieu": "co_dinh", "gia_tri": 6.0},
              {"ky_hieu": "trang_thai", "ten": "Công tắc (0 mở, 1 đóng)", "don_vi": "", "kieu": "dieu_chinh", "min": 0, "max": 1, "mac_dinh": 0, "buoc": 1},
              {"ky_hieu": "i_B", "ten": "Dòng cảm ứng trong cuộn B", "don_vi": "mA", "kieu": "tinh_ra"}],
  "mo_hinh": {"phuong_trinh": ["i_B khác 0 chỉ khi dòng trong cuộn A đang tăng (lúc đóng) hoặc đang giảm (lúc ngắt)",
                               "lúc đóng và lúc ngắt cho i_B ngược chiều nhau"],
              "gia_thiet": ["dòng trong cuộn A tăng tới giá trị ổn định trong một khoảng ngắn sau khi đóng", "bỏ qua từ trường Trái Đất"]},
  "so_lieu_mau": {"cot": ["Thời điểm", "Kim điện kế"],
                  "hang": [["công tắc mở", "0"], ["trong lúc đóng", "lệch phải rồi về 0"], ["giữ đóng", "0"],
                           ["trong lúc ngắt", "lệch trái rồi về 0"], ["sau khi ngắt", "0"]],
                  "ghi_chu": "Quan sát định tính; phía lệch tuỳ cách nối điện kế."},
  "ket_qua_ky_vong": "Kim chỉ lệch trong khoảnh khắc đóng và ngắt, hai lần ngược chiều nhau.",
  "hien_tuong_hay_sai": ["Nghĩ giữ công tắc đóng (nam châm điện đang mạnh) thì kim lệch mãi.", "Nghĩ lúc ngắt không có gì vì đã hết dòng điện."],
  "an_toan": "Không giữ công tắc đóng quá lâu để pin và cuộn dây không nóng.",
  "goi_y_mo_phong": {"loai": "do_thi", "y_tuong": "Bấm công tắc; vẽ đồng thời dòng trong cuộn A và kim điện kế của cuộn B theo thời gian.",
                     "diem_nhan": "Kim chỉ nhúc nhích ở hai sườn đồ thị dòng A, phần nằm ngang thì về 0."}})
tn.append({**base,
  "id": "tn-l9-camung-03", "ten": "Nam châm quay trước cuộn dây nối hai LED song song ngược chiều", "loai": "thi_nghiem", "muc_do": "co_ban",
  "kien_thuc": ["xoaychieu.khai_niem", "xoaychieu.nguyen_tac_tao", "camung.doi_chieu"],
  "muc_tieu": "Thấy hai LED ngược chiều thay nhau sáng, không sáng cùng lúc: dòng cảm ứng luân phiên đổi chiều, tức là dòng điện xoay chiều.",
  "dung_cu": [{"ten": "Nam châm thẳng trên giá có trục quay thẳng đứng", "so_luong": 1},
              {"ten": "Cuộn dây dẫn", "so_luong": 1},
              {"ten": "Hai đèn LED khác màu (đỏ, xanh) mắc song song, ngược chiều nhau", "so_luong": 2}],
  "cac_buoc": {"lam": ["Nối hai LED vào hai đầu cuộn dây như Hình 4.", "Quay nam châm đều và chậm trước cuộn dây.", "Quay nhanh hơn."],
               "quan_sat": ["Hai LED thay nhau chớp sáng, không bao giờ sáng cùng lúc.", "Quay nhanh hơn: chớp nhanh hơn, sáng hơn."],
               "rut_ra": ["Dòng cảm ứng luân phiên đổi chiều: đó là dòng điện xoay chiều.",
                          "Mỗi vòng quay, hai cực lần lượt đi qua trước cuộn dây nên dòng đổi chiều 2 lần."]},
  "tham_so": [{"ky_hieu": "n", "ten": "Số vòng quay mỗi giây", "don_vi": "vòng/s", "kieu": "dieu_chinh", "min": 0.5, "max": 5, "mac_dinh": 1, "buoc": 0.5},
              {"ky_hieu": "N_doi", "ten": "Số lần dòng đổi chiều mỗi giây", "don_vi": "lần/s", "kieu": "tinh_ra"}],
  "mo_hinh": {"phuong_trinh": ["N_doi = 2·n", "mỗi LED sáng trong nửa vòng quay"],
              "gia_thiet": ["nam châm hai cực, quay đều", "LED chỉ cho dòng đi qua theo một chiều"]},
  "so_lieu_mau": {"cot": ["n (vòng/s)", "Số lần đổi chiều mỗi giây", "Mỗi LED chớp mỗi giây"],
                  "hang": [[0.5, 1, 0.5], [1, 2, 1], [2, 4, 2]],
                  "ghi_chu": "Tính từ mô hình N_doi = 2n."},
  "ket_qua_ky_vong": "LED đỏ và LED xanh thay nhau sáng, mỗi đèn sáng nửa vòng quay.",
  "hien_tuong_hay_sai": ["Nghĩ hai LED cùng sáng vì cùng nối vào một cuộn dây.", "Nghĩ quay một chiều thì dòng điện cũng chỉ một chiều."],
  "an_toan": "Giữ tay xa nam châm đang quay.",
  "goi_y_mo_phong": {"loai": "2d_dong_hoc", "y_tuong": "Nam châm quay với tốc độ chỉnh được; hai LED sáng theo dấu dòng cảm ứng; tuỳ chọn hiện số đường sức qua cuộn dây.",
                     "diem_nhan": "Mỗi lần một cực quay qua chính diện cuộn dây, LED đang sáng tắt và LED kia sáng."}})
for dct in tn:
    p = ROOT / "content" / "thi-nghiem" / f"{dct['id']}.json"
    p.write_text(json.dumps(dct, ensure_ascii=False, indent=1), encoding="utf8")

print("ok", len(h), "| Hình 3: xa", n_xa, "gần", n_gan, "| bảng", [(t, round(tb, 2)) for t, _, tb, _ in rows])
